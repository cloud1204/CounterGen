"""
Benchmark Metamorphic_Agent across the Codeforces_Data/ corpus.

Two experiments share the same per-problem artifacts (validator + generator +
metamorphic relation), so the second runs at ~zero extra API cost:

`rounds` (R) = the number of INDEPENDENT metamorphic relations generated per problem.
Each relation is a fresh LLM generation, scored separately, so the metrics are
*per-relation* and measure how reliable a single generated relation is. `samples`
(S) = how many random inputs exercise each relation. (Deployment has no trusted
reference, so we never use the AC to filter relations -- it only labels ground truth.)

(A) Discrimination on human submissions (always on):
  - AC false-positive rate = fraction of the R relations that flag the human AC.
  - WA catch rate = fraction of the R relations that flag each WA (per-relation),
    plus the any-relation union (a WA caught if *any* of the R relations flags it).

(B) Golden-solution evaluation (opt-in via --goldens K):
  The real CounterGen workflow stress-tests candidate code against an *LLM-generated
  golden* (scripts/AC_generator.py). If that golden is silently wrong, the whole
  stress test is poisoned. The metamorphic relation is a candidate no-reference
  oracle for catching a bad golden. This mode asks whether it would be an upgrade:
    1. generate K independent first-edition LLM goldens (same prompt as AC_Agent),
       keeping only those that pass the existing gate (compile + example I/O);
    2. label each golden's ground-truth correctness by differential testing it
       against the trusted dataset AC.txt over many generator inputs;
    3. run the metamorphic relation on each golden (example-only AND generated-samples);
    4. report a confusion matrix -> base-rate-wrong (is the golden already ~always
       right? then the check is redundant), recall on wrong goldens (does the check
       catch them? else it is useless), and false-positive rate on correct goldens.

Layout expected:
  Codeforces_Data/difficulty_<N>/<contest>_<problem>/
    statement.txt or statement.md
    AC.txt
    WA1.txt, WA2.txt, ...

Usage:
  python -m tests.benchmark_metamorphic [--difficulty 2000] [--problem 2217_E]
                                        [--rounds 5] [--goldens 5] [--out results.md]
"""

import argparse
import contextlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import io
import json
import math
import multiprocessing as mp
import os
import queue as _queue
import random
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from utils.code import Code, split_output
from utils.agent import Agent
from utils.signal import Signal_Queue
from utils import usage
from scripts.validator import TC_Validator_Agent, Validator
from scripts.metamorphic import Metamorphic_Agent, Metamorphic
from scripts.generator import Generator_Agent
from scripts.checker import Checker, check_match
from scripts.AC_generator import AC_Agent
from tests.integration_metamorphic import load_credentials

DATA_DIR = "Codeforces_Data"
TMP_DIR = "tmp_storage"
CACHE_DIRNAME = ".bench_cache"

SLOW_THRESHOLD_SEC = 5.0
EXEC_TIMEOUT_SEC = 3
MAX_SHRINK_RETRIES = 5

# Statuses on a WA candidate that mean the WA was successfully identified.
# `caught` = metamorphic relation failed; the other three = the candidate
# crashed / timed out / didn't compile on the example input, which is itself
# proof the code is wrong.
_WA_CAUGHT_STATUSES = frozenset(
    {"caught", "exec-error", "exec-timeout", "compile-error"}
)


def _exec_timeout(deadline, cap=EXEC_TIMEOUT_SEC):
    """Subprocess timeout that never extends past the problem deadline, so a
    single candidate run can't overshoot the wall-clock budget. Returns `cap`
    when there's no deadline; otherwise min(cap, remaining), floored at a small
    positive value so a sliver of remaining budget still attempts a run (the
    caller's own deadline check stops the loop on the next iteration)."""
    if deadline is None:
        return cap
    rem = deadline - time.time()
    if rem <= 0:
        return 0.5
    return max(0.5, min(cap, rem))


@contextlib.contextmanager
def _quiet():
    """Silence stdout from chatty utility code (Code/Agent/Generator/Validator/
    Metamorphic all print verbosely). stderr is untouched so real errors still
    surface, and the captured buffer is dumped on exception for debugging."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            yield
    except BaseException:
        captured = buf.getvalue()
        if captured:
            tail = captured[-1500:]
            sys.__stdout__.write("\n---[ captured stdout before error ]---\n")
            sys.__stdout__.write(tail)
            if not tail.endswith("\n"):
                sys.__stdout__.write("\n")
            sys.__stdout__.write("---[ end captured ]---\n")
            sys.__stdout__.flush()
        raise


def cleanup_tmp_storage():
    if not os.path.isdir(TMP_DIR):
        return
    for name in os.listdir(TMP_DIR):
        path = os.path.join(TMP_DIR, name)
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass


_INPUT_BLOCK_RE = re.compile(r"\*\*Input:?\*\*\s*\n+```(?:\w*\n)?(.*?)```", re.DOTALL)
_OUTPUT_BLOCK_RE = re.compile(r"\*\*Output:?\*\*\s*\n+```(?:\w*\n)?(.*?)```", re.DOTALL)


def parse_problem(folder):
    statement_path = None
    for name in ("statement.txt", "statement.md"):
        p = os.path.join(folder, name)
        if os.path.exists(p):
            statement_path = p
            break
    if not statement_path:
        raise FileNotFoundError(f"No statement.{{txt,md}} in {folder}")
    with open(statement_path, encoding="utf-8") as f:
        statement = f.read()

    in_match = _INPUT_BLOCK_RE.search(statement)
    out_match = _OUTPUT_BLOCK_RE.search(statement)
    if not in_match or not out_match:
        raise ValueError(f"Could not extract first example I/O from {statement_path}")
    example_in = in_match.group(1).rstrip() + "\n"
    example_out = out_match.group(1).rstrip() + "\n"

    ac_path = os.path.join(folder, "AC.txt")
    if not os.path.exists(ac_path):
        raise FileNotFoundError(f"Missing AC.txt in {folder}")
    with open(ac_path, encoding="utf-8") as f:
        ac_text = f.read()

    wa_texts = []
    for fname in sorted(os.listdir(folder)):
        if re.fullmatch(r"WA\d+\.txt", fname):
            with open(os.path.join(folder, fname), encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                wa_texts.append((fname[:-4], content))

    return statement, example_in, example_out, ac_text, wa_texts


def _sample_random_input(
    generator: Code,
    args_limit,
    validator: Validator,
    max_attempts: int = 3,
    deadline=None,
):
    """Generate one validator-approved random input via the testcase generator.
    Returns the input string, or None if no attempt produced a valid input."""
    for _ in range(max_attempts):
        try:
            args = [random.randint(l, r) for l, r in args_limit]
            with _quiet():
                res = generator.execute(
                    input="1\n", args=args, timeout=_exec_timeout(deadline)
                )
        except Exception:
            continue
        if res == "timeout":
            continue
        if getattr(res, "stderr", "") or getattr(res, "returncode", 0) != 0:
            continue
        parts = split_output(res.stdout)
        if not parts:
            continue
        candidate = parts[0]
        try:
            with _quiet():
                ok = validator.validate(candidate).strip() == "valid"
            if ok:
                return candidate
        except Exception:
            continue
    return None


def _shrink_args_limit(args_limit):
    """Shrink each upper bound by integer sqrt (the same shape used by
    Generator_Agent's small_args_limits). Returns None if already at the
    lower bound everywhere."""
    if not args_limit:
        return None
    new = [(l, max(l, math.isqrt(max(r, 1)))) for l, r in args_limit]
    if all(a == b for a, b in zip(new, args_limit)):
        return None
    return new


def _run_one_sample(
    use_generator,
    generator,
    current_args,
    validator,
    example_in,
    code,
    meta,
    deadline=None,
):
    """Run one metamorphic sample. Returns (status, info):
    ('shrink', phase_description) -- a phase exceeded SLOW_THRESHOLD_SEC; caller
                                     should shrink args and retry the sample
    ('skip',   None)               -- couldn't produce a valid input/transform
    ('reason', reason_str)         -- caught a discrepancy
    ('pass',   None)               -- sample completed cleanly
    """
    if use_generator:
        base_in = _sample_random_input(
            generator, current_args, validator, deadline=deadline
        )
        if base_in is None:
            return "skip", None
    else:
        base_in = example_in

    t = time.time()
    with _quiet():
        base_run = code.execute(base_in, timeout=_exec_timeout(deadline))
    elapsed = time.time() - t
    if base_run == "timeout":
        return "shrink", f"candidate timed out (>{EXEC_TIMEOUT_SEC}s)"
    if elapsed > SLOW_THRESHOLD_SEC:
        return "shrink", f"candidate execution {elapsed:.1f}s"
    if getattr(base_run, "stderr", "") or getattr(base_run, "returncode", 0) != 0:
        return "reason", f"candidate crashed on input: {(base_run.stderr or '')[:150]}"
    base_out = base_run.stdout

    t = time.time()
    try:
        with _quiet():
            transformed = meta.transform(base_in)
    except Exception:
        return "skip", None
    elapsed = time.time() - t
    if elapsed > SLOW_THRESHOLD_SEC:
        return "shrink", f"metamorphic transform {elapsed:.1f}s"
    if not isinstance(transformed, str):
        return "skip", None
    try:
        with _quiet():
            valid_ok = validator.validate(transformed).strip() == "valid"
        if not valid_ok:
            return "skip", None
    except Exception:
        return "skip", None

    t = time.time()
    with _quiet():
        trans_run = code.execute(transformed, timeout=_exec_timeout(deadline))
    elapsed = time.time() - t
    if trans_run == "timeout":
        return (
            "shrink",
            f"candidate timed out on transformed input (>{EXEC_TIMEOUT_SEC}s)",
        )
    if elapsed > SLOW_THRESHOLD_SEC:
        return "shrink", f"candidate execution on transformed input {elapsed:.1f}s"
    if getattr(trans_run, "stderr", "") or getattr(trans_run, "returncode", 0) != 0:
        return (
            "reason",
            f"candidate crashed on transformed input: {(trans_run.stderr or '')[:150]}",
        )

    try:
        with _quiet():
            verdict = meta.relate(base_in, base_out, transformed, trans_run.stdout)
    except Exception:
        return "skip", None
    if isinstance(verdict, str) and verdict.strip() == "OK":
        return "pass", None
    return "reason", str(verdict)[:200]


def test_code(
    code_text,
    statement,
    example_in,
    example_out,
    meta,
    rounds,
    generator=None,
    args_limit=None,
    validator=None,
    samples_per_round=10,
    deadline=None,
):
    try:
        with _quiet():
            code = Code(code_text)
    except Exception as e:
        return {"status": "compile-error", "detail": str(e)[:300]}

    with _quiet():
        smoke = code.execute(example_in, timeout=_exec_timeout(deadline))
    if smoke == "timeout":
        return {"status": "exec-timeout"}
    if getattr(smoke, "stderr", "") or getattr(smoke, "returncode", 0) != 0:
        return {
            "status": "exec-error",
            "detail": (getattr(smoke, "stderr", "") or "")[:300],
        }

    use_generator = generator is not None and args_limit and validator is not None
    samples = samples_per_round if use_generator else 1
    current_args = (
        [tuple(x) for x in args_limit] if (use_generator and args_limit) else None
    )

    reasons = []
    rounds_run = 0
    rounds_skipped = 0

    truncated = False
    for _ in range(rounds):
        if deadline is not None and time.time() > deadline:
            truncated = True
            break
        for _ in range(samples):
            if deadline is not None and time.time() > deadline:
                truncated = True
                break
            shrink_attempts = 0
            while True:
                if deadline is not None and time.time() > deadline:
                    truncated = True
                    break
                try:
                    status, info = _run_one_sample(
                        use_generator,
                        generator,
                        current_args,
                        validator,
                        example_in,
                        code,
                        meta,
                        deadline=deadline,
                    )
                except Exception as e:
                    print(
                        f"  sample raised {type(e).__name__}: {str(e)[:200]}; skipping sample"
                    )
                    rounds_skipped += 1
                    break
                if status == "shrink":
                    if (
                        use_generator
                        and current_args is not None
                        and shrink_attempts < MAX_SHRINK_RETRIES
                    ):
                        new_args = _shrink_args_limit(current_args)
                        if new_args is not None:
                            print(
                                f"  slow run ({info}); shrinking args "
                                f"{current_args} -> {new_args}"
                            )
                            current_args = new_args
                            shrink_attempts += 1
                            continue
                    rounds_skipped += 1
                    break
                if status == "skip":
                    rounds_skipped += 1
                elif status == "reason":
                    reasons.append(info)
                    rounds_run += 1
                else:
                    rounds_run += 1
                break
        else:
            continue
        break

    total_attempts = rounds * samples
    result = {
        "rounds_total": total_attempts,
        "rounds_run": rounds_run,
        "rounds_skipped": rounds_skipped,
    }
    if truncated:
        result["truncated"] = True
    if reasons:
        result["status"] = "caught"
        result["rounds_caught"] = len(reasons)
        result["sample_reason"] = reasons[0]
    else:
        result["status"] = "pass"
    return result


def _cache_key(statement, example_in, example_out, model):
    h = hashlib.sha256()
    for s in (statement, example_in, example_out, model or ""):
        h.update(s.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:16]


def _cache_paths(folder, kind):
    cache_dir = os.path.join(folder, CACHE_DIRNAME)
    return (
        cache_dir,
        os.path.join(cache_dir, f"{kind}.py"),
        os.path.join(cache_dir, f"{kind}.key"),
    )


def _load_cached(folder, kind, key):
    _, code_path, key_path = _cache_paths(folder, kind)
    if not (os.path.exists(code_path) and os.path.exists(key_path)):
        return None
    with open(key_path, encoding="utf-8") as f:
        if f.read().strip() != key:
            return None
    with open(code_path, encoding="utf-8") as f:
        return f.read()


def _save_cached(folder, kind, key, code_text):
    cache_dir, code_path, key_path = _cache_paths(folder, kind)
    os.makedirs(cache_dir, exist_ok=True)
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code_text)
    with open(key_path, "w", encoding="utf-8") as f:
        f.write(key)


def _generate_validator(
    provider,
    api_key,
    model,
    statement,
    example_in,
    example_out,
    folder=None,
    cache_key=None,
    use_cache=True,
):
    """Build and return a working validator. Only successful validators are cached.
    On failure returns (None, failure_dict)."""
    if use_cache and folder and cache_key:
        cached_code = _load_cached(folder, "validator", cache_key)
        if cached_code is not None:
            try:
                with _quiet():
                    validator = Validator(Code(cached_code))
                    is_valid = validator.validate(example_in).strip() == "valid"
                if is_valid:
                    print(f"  validator: loaded from cache")
                    return validator, None
                print(f"  validator: cache stale (failed example), regenerating")
            except Exception as e:
                print(f"  validator: cache load failed ({e}), regenerating")

    sq = Signal_Queue()
    try:
        with _quiet():
            val_agent = Agent(sq, provider, api_key, model, "Validator")
            validator = TC_Validator_Agent(
                val_agent, statement, example_in, example_out
            ).work()
        print(f"  validator: built")
    except Exception as e:
        print(f"  validator gen failed: {e}")
        return None, {"stage": "validator", "error": str(e)[:300]}

    if use_cache and folder and cache_key:
        try:
            _save_cached(folder, "validator", cache_key, validator.code)
        except Exception as e:
            print(f"  validator: failed to save cache ({e})")
    return validator, None


def _gen_cache_paths(folder):
    cache_dir = os.path.join(folder, CACHE_DIRNAME)
    return (
        cache_dir,
        os.path.join(cache_dir, "generator.py"),
        os.path.join(cache_dir, "generator.key"),
        os.path.join(cache_dir, "generator.args.json"),
    )


def _load_cached_generator(folder, key):
    _, code_path, key_path, args_path = _gen_cache_paths(folder)
    if not all(os.path.exists(p) for p in (code_path, key_path, args_path)):
        return None
    with open(key_path, encoding="utf-8") as f:
        if f.read().strip() != key:
            return None
    with open(code_path, encoding="utf-8") as f:
        code_text = f.read()
    with open(args_path, encoding="utf-8") as f:
        args_limit = [tuple(x) for x in json.load(f)]
    return code_text, args_limit


def _save_cached_generator(folder, key, code_text, args_limit):
    cache_dir, code_path, key_path, args_path = _gen_cache_paths(folder)
    os.makedirs(cache_dir, exist_ok=True)
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code_text)
    with open(key_path, "w", encoding="utf-8") as f:
        f.write(key)
    with open(args_path, "w", encoding="utf-8") as f:
        json.dump(args_limit, f)


def _generate_testcase_generator(
    provider,
    api_key,
    model,
    validator,
    statement,
    example_in,
    folder=None,
    cache_key=None,
    use_cache=True,
):
    """Build and return (generator_code, args_limit). Only successful generators
    are cached. On failure returns (None, None, failure_dict)."""
    if use_cache and folder and cache_key:
        cached = _load_cached_generator(folder, cache_key)
        if cached is not None:
            code_text, args_limit = cached
            try:
                with _quiet():
                    gen_code = Code(code_text)
                    args = [l for l, _ in args_limit]
                    res = gen_code.execute(input="1\n", args=args, timeout=15)
                    ok = (
                        res != "timeout"
                        and not getattr(res, "stderr", "")
                        and getattr(res, "returncode", 0) == 0
                    )
                    parts_ok = False
                    if ok:
                        parts = split_output(res.stdout)
                        if parts and validator.validate(parts[0]).strip() == "valid":
                            parts_ok = True
                if parts_ok:
                    print(f"  generator: loaded from cache")
                    return gen_code, args_limit, None
                print(f"  generator: cache stale, regenerating")
            except Exception as e:
                print(f"  generator: cache load failed ({e}), regenerating")

    sq = Signal_Queue()
    try:
        with _quiet():
            gen_agent = Agent(sq, provider, api_key, model, "Generator")
            ga = Generator_Agent(gen_agent, statement, example_in)
            ga.generate_first_edition()
            gen_code, args_limit = ga.finalize(validator=validator)
        print(f"  generator: built (args_limit={args_limit})")
    except Exception as e:
        print(f"  generator gen failed: {e}")
        return None, None, {"stage": "generator", "error": str(e)[:300]}

    if use_cache and folder and cache_key:
        try:
            _save_cached_generator(folder, cache_key, gen_code.code, args_limit)
        except Exception as e:
            print(f"  generator: failed to save cache ({e})")
    return gen_code, args_limit, None


def _generate_metamorphic_with_validator(
    provider, api_key, model, validator, statement, example_in, example_out, quiet=True
):
    """One metamorphic attempt against an already-built validator. Always regenerated;
    never cached, because the transform is intentionally randomized per run.

    `quiet=False` skips the internal stdout redirect (for use under a single
    pool-level _quiet(); see _generate_golden for why per-thread redirect is unsafe)."""
    suppress = _quiet if quiet else contextlib.nullcontext
    sq = Signal_Queue()
    try:
        with suppress():
            meta_agent = Agent(sq, provider, api_key, model, "Metamorphic")
            meta = Metamorphic_Agent(
                meta_agent, statement, example_in, example_out
            ).generate(validator)
    except Exception as e:
        print(f"  metamorphic gen failed: {e}")
        return None, {"stage": "metamorphic", "error": str(e)[:300]}
    if meta is None:
        print("  metamorphic: LLM declined to provide a relation")
        return None, {"stage": "declined"}
    print("  metamorphic: built")
    return meta, None


def _generate_one_relation(
    provider,
    api_key,
    model,
    validator,
    statement,
    example_in,
    example_out,
    attempts,
    deadline=None,
    quiet=True,
):
    """Generate a single usable relation, retrying up to `attempts` times on
    decline/error. Returns (meta, failure)."""
    meta, failure = None, None
    for _ in range(max(1, attempts)):
        if deadline is not None and time.time() > deadline:
            break
        meta, failure = _generate_metamorphic_with_validator(
            provider,
            api_key,
            model,
            validator,
            statement,
            example_in,
            example_out,
            quiet=quiet,
        )
        if meta is not None:
            break
    return meta, failure


def _generate_relations_parallel(
    provider,
    api_key,
    model,
    validator,
    statement,
    example_in,
    example_out,
    rounds,
    attempts,
    workers=2,
    deadline=None,
):
    """Generate R independent relations concurrently (network-bound LLM calls).
    Returns {round_index (1-based): (meta, failure)}. Output suppressed under a
    single pool-level _quiet() (workers run quiet=False)."""
    if rounds <= 0:
        return {}
    n_workers = max(1, min(workers, rounds))
    out = {}
    with _quiet():
        with ThreadPoolExecutor(max_workers=n_workers) as ex:
            futs = {
                ex.submit(
                    _generate_one_relation,
                    provider,
                    api_key,
                    model,
                    validator,
                    statement,
                    example_in,
                    example_out,
                    attempts,
                    deadline=deadline,
                    quiet=False,
                ): r
                for r in range(1, rounds + 1)
            }
            for fut in as_completed(futs):
                r = futs[fut]
                try:
                    out[r] = fut.result()
                except Exception as e:
                    out[r] = (None, {"stage": "metamorphic", "error": str(e)[:300]})
    return out


def _check_compiles(label, code_text):
    """Try to construct a Code() to verify it compiles. Returns (ok, error_str)."""
    try:
        with _quiet():
            Code(code_text)
        return True, None
    except Exception as e:
        return False, f"{type(e).__name__}: {str(e)[:200]}"


# --------------------------------------------------------------------------
# Golden-solution evaluation (experiment B). Everything below operates on the
# already-built per-problem artifacts, so it costs no extra LLM tokens beyond
# generating the K goldens and the checker.
# --------------------------------------------------------------------------

_CHECKER_BUILTIN_SENTINEL = "# BUILTIN check_match"


def _meta_flagged(result):
    """True if a metamorphic test_code() result counts as flagging the code."""
    return result.get("status") in _WA_CAUGHT_STATUSES


def _meta_verdict(result):
    """Reduce a test_code() result to 'flag' / 'pass' / 'na' for confusion tallying."""
    if _meta_flagged(result):
        return "flag"
    if result.get("status") == "pass":
        return "pass"
    return "na"


def _build_checker_from_source(src):
    """Reconstruct a Checker from cached source (or the builtin sentinel)."""
    chk = Checker()
    if src.strip() == _CHECKER_BUILTIN_SENTINEL:
        chk.checker_func = check_match
    else:
        ns = {}
        exec(src, ns)
        if "check" not in ns:
            raise ValueError("cached checker source defines no check()")
        chk.checker_func = ns["check"]
    return chk


def _generate_checker(
    provider, api_key, model, statement, folder=None, cache_key=None, use_cache=True
):
    """Build a Checker for ground-truth labeling, mirroring
    Checker.customize_checker_if_needed but capturing the source so it can be
    cached. Falls back to the builtin check_match on any failure."""
    if use_cache and folder and cache_key:
        cached = _load_cached(folder, "checker", cache_key)
        if cached is not None:
            try:
                chk = _build_checker_from_source(cached)
                print("  checker: loaded from cache")
                return chk
            except Exception as e:
                print(f"  checker: cache load failed ({e}), regenerating")

    src = _CHECKER_BUILTIN_SENTINEL
    chk = Checker()
    chk.checker_func = check_match
    sq = Signal_Queue()
    try:
        with _quiet():
            agent = Agent(sq, provider, api_key, model, "Checker")
            with open("instruction_texts/advanced_checker_requirement.txt") as f:
                requirement_query = f.read()
            response = agent.instruct(f"{statement}\n{requirement_query}")
            if "No" not in response[:10]:
                with open("instruction_texts/advanced_checker_gen.txt") as f:
                    prompt = f.read()
                code_obj = agent.instruct(prompt=prompt, code_only=True)
                src = code_obj.code
                chk = _build_checker_from_source(src)
        print(
            "  checker: built"
            + (" (builtin)" if src == _CHECKER_BUILTIN_SENTINEL else " (custom)")
        )
    except Exception as e:
        print(f"  checker gen failed ({e}); falling back to builtin check_match")
        src = _CHECKER_BUILTIN_SENTINEL
        chk = Checker()
        chk.checker_func = check_match

    if use_cache and folder and cache_key:
        try:
            _save_cached(folder, "checker", cache_key, src)
        except Exception as e:
            print(f"  checker: failed to save cache ({e})")
    return chk


def _generate_golden(
    provider,
    api_key,
    model,
    statement,
    example_in,
    example_out,
    index,
    folder=None,
    cache_key=None,
    use_cache=True,
    quiet=True,
):
    """Generate one first-edition LLM golden via the real AC_Agent prompt (no
    regeneration loop -- we want an honest sample of first-edition quality).
    Cached per index so re-runs replay the same goldens. Returns a Code or None.

    `quiet=False` skips the internal stdout redirect; pass it when running many
    of these concurrently (the caller holds a single _quiet() for the whole pool,
    because _quiet() redirects sys.stdout process-globally and is not safe to
    nest across threads)."""
    suppress = _quiet if quiet else contextlib.nullcontext
    kind = f"golden_{index}"
    if use_cache and folder and cache_key:
        cached = _load_cached(folder, kind, cache_key)
        if cached is not None:
            try:
                with suppress():
                    code_obj = Code(cached)
                print(f"  golden {index}: loaded from cache")
                return code_obj
            except Exception as e:
                print(f"  golden {index}: cache load failed ({e}), regenerating")

    sq = Signal_Queue()
    try:
        with suppress():
            agent = Agent(sq, provider, api_key, model, f"AC-{index}")
            ac_agent = AC_Agent(agent, statement, example_in, example_out)
            ac_agent.generate_first_edition()
            code_obj = ac_agent.AC_code
    except Exception as e:
        print(f"  golden {index}: generation failed ({e})")
        return None
    if not isinstance(code_obj, Code):
        print(f"  golden {index}: generation returned no Code")
        return None

    if use_cache and folder and cache_key:
        try:
            _save_cached(folder, kind, cache_key, code_obj.code)
        except Exception as e:
            print(f"  golden {index}: failed to save cache ({e})")
    return code_obj


def _generate_goldens_parallel(
    provider,
    api_key,
    model,
    statement,
    example_in,
    example_out,
    num_goldens,
    folder=None,
    cache_key=None,
    use_cache=True,
    workers=2,
):
    """Generate the K goldens concurrently -- they're independent, network-bound
    LLM calls, so threads overlap the latency well. Returns {index: Code or None}.

    Worker output is suppressed under a SINGLE _quiet() on this thread (workers
    run with quiet=False); per-thread stdout redirects would race because
    redirect_stdout swaps sys.stdout process-globally."""
    if num_goldens <= 0:
        return {}
    n_workers = max(1, min(workers, num_goldens))
    results = {}
    with _quiet():
        with ThreadPoolExecutor(max_workers=n_workers) as ex:
            futs = {
                ex.submit(
                    _generate_golden,
                    provider,
                    api_key,
                    model,
                    statement,
                    example_in,
                    example_out,
                    i,
                    folder=folder,
                    cache_key=cache_key,
                    use_cache=use_cache,
                    quiet=False,
                ): i
                for i in range(num_goldens)
            }
            for fut in as_completed(futs):
                i = futs[fut]
                try:
                    results[i] = fut.result()
                except Exception:
                    results[i] = None
    return results


def _existing_gate(code_obj, example_in, example_out, checker, deadline=None):
    """Replicate AC_generator.test()'s pre-metamorphic gate: the golden must run
    on the example input and the checker must accept its output. Returns
    (passed: bool, reason: str)."""
    with _quiet():
        run = code_obj.execute(example_in, timeout=_exec_timeout(deadline))
    if run == "timeout":
        return False, "exec-timeout on example"
    if getattr(run, "stderr", "") or getattr(run, "returncode", 0) != 0:
        return (
            False,
            f"exec-error on example: {(getattr(run, 'stderr', '') or '')[:150]}",
        )
    try:
        verdict = checker.check(example_in, run.stdout, example_out)
    except Exception as e:
        return False, f"checker raised: {e}"
    if verdict != "AC":
        return False, f"example WA: {str(verdict)[:150]}"
    return True, "pass"


def _compare_on_input(golden, ac_code, checker, inp, timeout=EXEC_TIMEOUT_SEC):
    """Differential-test a golden against the trusted reference on one input.
    Returns (verdict, reason):
      'agree'    -- golden completed and the checker accepts its output vs the reference
      'mismatch' -- golden completed but the checker rejected it (a definitive wrong answer)
      'tle'      -- golden timed out (a speed failure, shrinkable)
      'crash'    -- golden errored at runtime (treated like tle: may be scale-dependent)
      'skip'     -- reference itself failed; cannot judge this input
    """
    with _quiet():
        ref = ac_code.execute(inp, timeout=timeout)
    if (
        ref == "timeout"
        or getattr(ref, "stderr", "")
        or getattr(ref, "returncode", 0) != 0
    ):
        return "skip", "reference failed"
    with _quiet():
        got = golden.execute(inp, timeout=timeout)
    if got == "timeout":
        return "tle", "golden timed out"
    if getattr(got, "stderr", "") or getattr(got, "returncode", 0) != 0:
        return "crash", f"golden crashed: {(got.stderr or '')[:150]}"
    try:
        # checker.check(Input, outA, outB): outB is treated as correct.
        verdict = checker.check(inp, got.stdout, ref.stdout)
    except Exception as e:
        return "skip", f"checker raised: {e}"
    if verdict == "AC":
        return "agree", ""
    return "mismatch", f"output mismatch: {str(verdict)[:200]}"


def _label_golden(
    golden,
    ac_code,
    generator,
    args_limit,
    validator,
    checker,
    example_in,
    num_inputs,
    deadline=None,
):
    """Ground-truth label a golden by differential testing against the trusted
    reference (dataset AC.txt). Returns (label, witness):
      'wrong-answer' -- golden COMPLETED but produced a wrong answer (definitive;
                        this is what the metamorphic check should catch)
      'correct'      -- agreed with the reference and never timed out within the
                        problem's input bounds (strong evidence, not a proof)
      'slow'         -- agreed where it completed but timed out (or errored) on a
                        full-size input; a speed/scale failure, NOT a wrong answer.
                        Out of the metamorphic check's scope, and the stress tester
                        already detects a slow reference on its own.
      'unknown'      -- never obtained a usable comparison (reference kept failing
                        / no valid inputs produced)

    On a TLE we SHRINK the generator args and re-draw a smaller input, so a
    correct-but-slow brute force is distinguished from a logically wrong one --
    and, importantly, a wrong answer hiding behind a TLE at full size can still be
    caught on the smaller instance. Only a checker mismatch on a run the golden
    actually completed counts as 'wrong-answer'."""
    seen_agree = False
    seen_incomplete = False  # timed out / errored on some full-size input

    verdict, reason = _compare_on_input(
        golden, ac_code, checker, example_in, timeout=_exec_timeout(deadline)
    )
    if verdict == "mismatch":
        return "wrong-answer", f"on example input: {reason}"
    if verdict == "agree":
        seen_agree = True
    elif verdict in ("tle", "crash"):
        seen_incomplete = True  # example is fixed-size, can't shrink it

    use_generator = generator is not None and args_limit and validator is not None
    if use_generator:
        current_args = [tuple(x) for x in args_limit]
        for _ in range(num_inputs):
            if deadline is not None and time.time() > deadline:
                break
            shrinks = 0
            while True:
                if deadline is not None and time.time() > deadline:
                    break
                inp = _sample_random_input(
                    generator, current_args, validator, deadline=deadline
                )
                if inp is None:
                    break
                verdict, reason = _compare_on_input(
                    golden, ac_code, checker, inp, timeout=_exec_timeout(deadline)
                )
                if verdict == "mismatch":
                    return "wrong-answer", f"{reason}\non input:\n{inp[:300]}"
                if verdict == "agree":
                    seen_agree = True
                    break
                if verdict == "skip":
                    break
                # tle / crash: the golden may just be slow at this size. Shrink the
                # args and retry so we can still check correctness on a smaller
                # instance (and surface a wrong answer if one is hiding there).
                seen_incomplete = True
                new_args = (
                    _shrink_args_limit(current_args)
                    if shrinks < MAX_SHRINK_RETRIES
                    else None
                )
                if new_args is None:
                    break
                current_args = new_args
                shrinks += 1

    # A demonstrated timeout within the problem's bounds makes it 'slow' even if it
    # also agreed on smaller inputs; only a clean, never-timed-out golden is 'correct'.
    if seen_incomplete:
        return "slow", ""
    if seen_agree:
        return "correct", ""
    return "unknown", ""


def _build_golden_corpus(
    provider,
    api_key,
    model,
    statement,
    example_in,
    example_out,
    ac_code,
    generator,
    args_limit,
    validator,
    checker,
    num_goldens,
    label_inputs,
    folder=None,
    cache_key=None,
    use_cache=True,
    deadline=None,
    gen_workers=2,
):
    """Generate K goldens, apply the existing gate, and ground-truth-label the
    gate-passers against the trusted AC.txt. This is relation-independent, so it
    runs once per problem. Gate-pass records carry 'code_text' and empty verdict
    lists ('meta_example_verdicts' / 'meta_samples_verdicts') to be filled in by
    each relation round.

    The K LLM generations run in parallel (gen_workers threads); gating and
    labeling stay sequential because they spawn CPU-bound subprocesses."""
    # Report cache status up front: the per-golden "loaded from cache" prints
    # happen inside the parallel pool's _quiet() and are suppressed, so without
    # this it looks like all K are being regenerated.
    cached_n = 0
    if use_cache and folder and cache_key:
        cached_n = sum(
            1
            for i in range(num_goldens)
            if _load_cached(folder, f"golden_{i}", cache_key) is not None
        )
    to_gen = num_goldens - cached_n
    if to_gen == 0:
        print(f"  goldens: all {num_goldens} loaded from cache (no generation)")
    elif cached_n:
        print(
            f"  goldens: {cached_n}/{num_goldens} cached, generating {to_gen} fresh "
            f"({min(gen_workers, to_gen)} parallel workers)..."
        )
    else:
        print(
            f"  generating {num_goldens} goldens ({min(gen_workers, num_goldens)} parallel workers)..."
        )
    generated = _generate_goldens_parallel(
        provider,
        api_key,
        model,
        statement,
        example_in,
        example_out,
        num_goldens,
        folder=folder,
        cache_key=cache_key,
        use_cache=use_cache,
        workers=gen_workers,
    )

    corpus = []
    for i in range(num_goldens):
        if deadline is not None and time.time() > deadline:
            print(f"  golden corpus: deadline hit after {i} goldens (gate/label phase)")
            break
        rec = {"index": i}
        code_obj = generated.get(i)
        if code_obj is None:
            rec["gate"] = "gen-failed"
            corpus.append(rec)
            continue

        passed, reason = _existing_gate(
            code_obj, example_in, example_out, checker, deadline=deadline
        )
        if not passed:
            rec["gate"] = "fail"
            rec["gate_reason"] = reason
            print(f"  golden {i}: failed existing gate -- {reason}")
            corpus.append(rec)
            continue
        rec["gate"] = "pass"

        label, witness = _label_golden(
            code_obj,
            ac_code,
            generator,
            args_limit,
            validator,
            checker,
            example_in,
            label_inputs,
            deadline=deadline,
        )
        rec["ground_truth"] = label
        if witness:
            rec["gt_witness"] = witness[:300]
        rec["code_text"] = code_obj.code
        rec["meta_example_verdicts"] = []
        rec["meta_samples_verdicts"] = []
        print(f"  golden {i}: gate=pass truth={label}")
        corpus.append(rec)
    return corpus


def _score_relation_on_goldens(
    corpus,
    meta,
    statement,
    example_in,
    example_out,
    generator,
    args_limit,
    validator,
    samples,
    deadline=None,
):
    """Append ONE relation's verdict (example-only and generated-samples) to each
    gate-pass golden in the corpus. Called once per relation round."""
    use_gen = generator is not None and args_limit and validator is not None
    for g in corpus:
        if g.get("gate") != "pass":
            continue
        ex = test_code(
            g["code_text"],
            statement,
            example_in,
            example_out,
            meta,
            1,
            generator=None,
            args_limit=None,
            validator=None,
            samples_per_round=samples,
            deadline=deadline,
        )
        g["meta_example_verdicts"].append(_meta_verdict(ex))
        if use_gen:
            sm = test_code(
                g["code_text"],
                statement,
                example_in,
                example_out,
                meta,
                1,
                generator=generator,
                args_limit=args_limit,
                validator=validator,
                samples_per_round=samples,
                deadline=deadline,
            )
            g["meta_samples_verdicts"].append(_meta_verdict(sm))
        else:
            g["meta_samples_verdicts"].append("na")


def _confusion_rates(tp, fp, fn, tn):
    judged = tp + fp + fn + tn
    wrong = tp + fn
    correct = fp + tn
    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "judged": judged,
        "wrong": wrong,
        "correct": correct,
        "recall": (tp / wrong) if wrong else None,
        "fp_rate": (fp / correct) if correct else None,
    }


def _iter_scored_goldens(results):
    """Yield gate-pass goldens whose ground truth is decisive for the confusion
    matrix: 'wrong-answer' or 'correct'. 'slow' and 'unknown' are excluded -- the
    metamorphic check is not expected to catch a slow-but-correct golden, so
    scoring it would only manufacture noise."""
    for r in results:
        gr = r.get("goldens")
        if not gr:
            continue
        for g in gr.get("corpus", []):
            if g.get("gate") != "pass":
                continue
            if g.get("ground_truth") in ("wrong-answer", "correct"):
                yield g


def _golden_pair_confusion(results, variant_key):
    """Per-(relation, golden) confusion: every relation's verdict on every
    gate-pass, decisively-labeled golden is one observation. NO AC-based filtering.
    'wrong-answer' is the positive class; 'slow'/'unknown' are excluded entirely.
    variant_key in {'meta_example_verdicts', 'meta_samples_verdicts'}."""
    tp = fp = fn = tn = 0
    for g in _iter_scored_goldens(results):
        wrong = g["ground_truth"] == "wrong-answer"
        for v in g.get(variant_key, []):
            if v not in ("flag", "pass"):
                continue
            flagged = v == "flag"
            if wrong:
                tp += flagged
                fn += not flagged
            else:
                fp += flagged
                tn += not flagged
    return _confusion_rates(tp, fp, fn, tn)


def _golden_union_confusion(results, variant_key):
    """Per-golden union: a golden is flagged if ANY of the R relations flagged it.
    The optimistic 'best of R relations' number."""
    tp = fp = fn = tn = 0
    for g in _iter_scored_goldens(results):
        verdicts = [v for v in g.get(variant_key, []) if v in ("flag", "pass")]
        if not verdicts:
            continue
        flagged = any(v == "flag" for v in verdicts)
        wrong = g["ground_truth"] == "wrong-answer"
        if wrong:
            tp += flagged
            fn += not flagged
        else:
            fp += flagged
            tn += not flagged
    return _confusion_rates(tp, fp, fn, tn)


def _golden_population(results):
    """Relation-independent golden census: generation / gate / ground-truth
    counts. base_rate_wrong is computed over DECISIVE goldens (wrong-answer +
    correct); 'slow' is tracked separately (correct-but-too-slow / TLE)."""
    generated = gate_passed = wrong = correct = slow = unknown = 0
    for r in results:
        gr = r.get("goldens")
        if not gr:
            continue
        for g in gr.get("corpus", []):
            generated += 1
            if g.get("gate") == "pass":
                gate_passed += 1
                gt = g.get("ground_truth")
                if gt == "wrong-answer":
                    wrong += 1
                elif gt == "correct":
                    correct += 1
                elif gt == "slow":
                    slow += 1
                else:
                    unknown += 1
    judged = wrong + correct
    return {
        "generated": generated,
        "gate_passed": gate_passed,
        "wrong": wrong,
        "correct": correct,
        "slow": slow,
        "unknown": unknown,
        "judged": judged,
        "base_rate_wrong": (wrong / judged) if judged else None,
    }


def _run_problem_inner(
    folder,
    provider,
    api_key,
    model,
    rounds,
    attempts,
    use_cache=True,
    use_generator=True,
    samples_per_round=10,
    problem_timeout=300.0,
    num_goldens=0,
    label_inputs=20,
    gen_workers=2,
):
    t0 = time.time()
    deadline = (
        (t0 + problem_timeout) if problem_timeout and problem_timeout > 0 else None
    )

    def _tle(stage):
        elapsed = time.time() - t0
        print(
            f"  time limit exceeded during {stage} ({elapsed:.1f}s > {problem_timeout}s); skipping problem"
        )
        return {
            "problem": folder,
            "status": "time-limit-exceeded",
            "stage": stage,
            "time": elapsed,
        }

    try:
        statement, example_in, example_out, ac_text, wa_texts = parse_problem(folder)
    except Exception as e:
        print(f"  parse failed: {e}")
        return {"problem": folder, "status": "parse-error", "error": str(e)}

    compile_errors = {}
    ok, err = _check_compiles("AC", ac_text)
    if not ok:
        compile_errors["AC"] = err
    for label, text in wa_texts:
        ok, err = _check_compiles(label, text)
        if not ok:
            compile_errors[label] = err
    cleanup_tmp_storage()
    if compile_errors:
        for label, err in compile_errors.items():
            print(f"  {label}: compile failed -- {err}")
        print(f"  skipping problem (no LLM tokens spent)")
        return {
            "problem": folder,
            "status": "compile-check-failed",
            "compile_errors": compile_errors,
            "time": time.time() - t0,
        }

    key = _cache_key(statement, example_in, example_out, model)
    validator, val_failure = _generate_validator(
        provider,
        api_key,
        model,
        statement,
        example_in,
        example_out,
        folder=folder,
        cache_key=key,
        use_cache=use_cache,
    )
    if validator is None:
        return {
            "problem": folder,
            "status": "validator-error",
            "attempts_tried": 0,
            "failures": [{"attempt": 0, **val_failure}],
            "time": time.time() - t0,
        }

    if deadline is not None and time.time() > deadline:
        return _tle("validator")

    gen_code, args_limit = None, None
    if use_generator:
        gen_code, args_limit, gen_failure = _generate_testcase_generator(
            provider,
            api_key,
            model,
            validator,
            statement,
            example_in,
            folder=folder,
            cache_key=key,
            use_cache=use_cache,
        )
        if gen_code is None:
            print(
                "  generator unavailable; falling back to example input only for metamorphic rounds"
            )

    if deadline is not None and time.time() > deadline:
        return _tle("generator")

    # Build the golden corpus once (relation-independent): generate K goldens,
    # gate them, ground-truth-label against AC.txt. Done before the relation loop
    # so every relation is scored against the same corpus.
    golden_corpus = None
    if num_goldens > 0:
        if deadline is not None and time.time() > deadline:
            return _tle("before-goldens")
        try:
            with _quiet():
                ac_code = Code(ac_text)
        except Exception as e:
            print(
                f"  golden eval: reference AC.txt failed to build ({e}); skipping goldens"
            )
            ac_code = None
        if ac_code is not None:
            checker = _generate_checker(
                provider,
                api_key,
                model,
                statement,
                folder=folder,
                cache_key=key,
                use_cache=use_cache,
            )
            golden_corpus = _build_golden_corpus(
                provider,
                api_key,
                model,
                statement,
                example_in,
                example_out,
                ac_code,
                gen_code,
                args_limit,
                validator,
                checker,
                num_goldens=num_goldens,
                label_inputs=label_inputs,
                folder=folder,
                cache_key=key,
                use_cache=use_cache,
                deadline=deadline,
                gen_workers=gen_workers,
            )

    def _safe_test(label, code_text, meta):
        try:
            return test_code(
                code_text,
                statement,
                example_in,
                example_out,
                meta,
                1,
                generator=gen_code,
                args_limit=args_limit,
                validator=validator,
                samples_per_round=samples_per_round,
                deadline=deadline,
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            print(
                f"  {label}: test_code raised {type(e).__name__}; recording as test-error"
            )
            return {
                "status": "test-error",
                "detail": f"{type(e).__name__}: {str(e)[:300]}",
            }

    # Relation trials: `rounds` = R INDEPENDENT relation generations. Each relation
    # is scored against the human AC, every WA, and the golden corpus. Metrics are
    # per-relation (no AC-based filtering): how does a single generated relation
    # behave? `samples_per_round` is how many random inputs exercise each relation.
    #
    # Phase 1 -- generate all R relations in parallel (network-bound LLM calls).
    # Phase 2 -- score each sequentially (subprocess-bound; deadline-truncatable).
    relation_failures = []
    ac_verdicts = []
    ac_fp_reason = None
    wa_labels = [label for label, _ in wa_texts]
    wa_verdicts = {label: [] for label in wa_labels}
    wa_reasons = {}
    relations_valid = relations_declined = relations_errored = 0
    relations_truncated = False

    if deadline is not None and time.time() > deadline:
        gen_results = {}
        relations_truncated = True
    else:
        print(
            f"  generating {rounds} relations ({min(gen_workers, rounds)} parallel workers)..."
        )
        gen_results = _generate_relations_parallel(
            provider,
            api_key,
            model,
            validator,
            statement,
            example_in,
            example_out,
            rounds,
            attempts,
            workers=gen_workers,
            deadline=deadline,
        )

    for r in range(1, rounds + 1):
        if r not in gen_results:
            continue  # never generated (deadline hit before phase 1)
        if deadline is not None and time.time() > deadline:
            relations_truncated = True
            print(f"  scoring phase: deadline hit before relation {r}")
            break
        meta, failure = gen_results[r]
        if meta is None:
            stage = (failure or {}).get("stage", "unknown")
            if stage == "declined":
                relations_declined += 1
            else:
                relations_errored += 1
            relation_failures.append({"round": r, **(failure or {})})
            print(f"  relation {r}/{rounds}: no relation ({stage})")
            continue
        relations_valid += 1

        ac_res = _safe_test("AC", ac_text, meta)
        ac_v = _meta_verdict(ac_res)
        ac_verdicts.append(ac_v)
        if ac_v == "flag" and ac_fp_reason is None:
            ac_fp_reason = ac_res.get("sample_reason") or ac_res.get("detail") or ""

        for label, text in wa_texts:
            if deadline is not None and time.time() > deadline:
                break
            res = _safe_test(label, text, meta)
            v = _meta_verdict(res)
            wa_verdicts[label].append(v)
            if v == "flag" and label not in wa_reasons:
                wa_reasons[label] = res.get("sample_reason") or res.get("detail") or ""

        if golden_corpus is not None and not (
            deadline is not None and time.time() > deadline
        ):
            _score_relation_on_goldens(
                golden_corpus,
                meta,
                statement,
                example_in,
                example_out,
                gen_code,
                args_limit,
                validator,
                samples_per_round,
                deadline=deadline,
            )

        wa_flag_now = sum(
            1 for l in wa_labels if wa_verdicts[l] and wa_verdicts[l][-1] == "flag"
        )
        print(
            f"  relation {r}/{rounds} scored: AC={ac_v}  WA-flagged={wa_flag_now}/{len(wa_labels)}"
        )

    golden_block = None
    if golden_corpus is not None:
        golden_block = {
            "num_goldens": len(golden_corpus),
            "gate_passed": sum(1 for g in golden_corpus if g.get("gate") == "pass"),
            "corpus": golden_corpus,
        }

    # No relation ever produced -> surface why (still attach any built corpus).
    if relations_valid == 0:
        last = relation_failures[-1] if relation_failures else {}
        stage = last.get("stage", "unknown")
        status = (
            "time-limit-exceeded"
            if relations_truncated
            else {"declined": "declined"}.get(stage, "metamorphic-error")
        )
        out = {
            "problem": folder,
            "status": status,
            "relations_requested": rounds,
            "relations_valid": 0,
            "relations_declined": relations_declined,
            "relations_errored": relations_errored,
            "relation_failures": relation_failures,
            "time": time.time() - t0,
        }
        if golden_block is not None:
            out["goldens"] = golden_block
        return out

    ac_fp_count = sum(1 for v in ac_verdicts if v == "flag")
    wa_union_caught = sum(
        1 for l in wa_labels if any(v == "flag" for v in wa_verdicts[l])
    )
    print(
        f"  AC false-positive: {ac_fp_count}/{relations_valid} relations flagged the human AC"
    )
    print(f"  WA caught by >=1 relation: {wa_union_caught}/{len(wa_labels)}")

    result = {
        "problem": folder,
        "status": "time-limit-exceeded" if relations_truncated else "ok",
        "time": time.time() - t0,
        "relations_requested": rounds,
        "relations_valid": relations_valid,
        "relations_declined": relations_declined,
        "relations_errored": relations_errored,
        "relation_failures": relation_failures,
        "ac_verdicts": ac_verdicts,
        "ac_fp_count": ac_fp_count,
        "ac_fp_reason": ac_fp_reason,
        "wa_labels": wa_labels,
        "wa_verdicts": wa_verdicts,
        "wa_reasons": wa_reasons,
    }
    if golden_block is not None:
        result["goldens"] = golden_block
        pop = _golden_population([result])
        print(
            f"  golden corpus: {pop['gate_passed']}/{pop['generated']} passed gate; "
            f"ground truth wrong-answer={pop['wrong']} correct={pop['correct']} "
            f"slow={pop['slow']} unknown={pop['unknown']}"
        )
    return result


def run_problem(
    folder,
    provider,
    api_key,
    model,
    rounds,
    attempts=1,
    use_cache=True,
    use_generator=True,
    samples_per_round=10,
    problem_timeout=300.0,
    num_goldens=0,
    label_inputs=20,
    gen_workers=2,
    cost_cap=None,
    call_cap=None,
):
    t0 = time.time()
    usage.reset()  # this run's API spend for this problem only (cache hits cost nothing)
    usage.set_budget(cost_cap)  # cumulative per-problem $ cap; gates every LLM call
    usage.set_call_cap(call_cap)  # per-single-call $ ceiling; refuses a runaway call
    try:
        res = _run_problem_inner(
            folder,
            provider,
            api_key,
            model,
            rounds,
            attempts,
            use_cache=use_cache,
            use_generator=use_generator,
            samples_per_round=samples_per_round,
            problem_timeout=problem_timeout,
            num_goldens=num_goldens,
            label_inputs=label_inputs,
            gen_workers=gen_workers,
        )
    except KeyboardInterrupt:
        raise
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"  unhandled exception in problem; recording and moving on")
        res = {
            "problem": folder,
            "status": "unhandled-error",
            "error": f"{type(e).__name__}: {str(e)[:300]}",
            "time": time.time() - t0,
        }
    finally:
        cleanup_tmp_storage()
    res["api_usage"] = usage.snapshot()
    res["cost_limited"] = usage.over_budget()
    u = res["api_usage"]
    cap_note = "  [COST CAP HIT]" if res["cost_limited"] else ""
    print(
        f"  API usage: {u['calls']} calls, {u['total_tokens']} tokens"
        + (f", ${u['cost']:.4f}" if u.get("cost") else "")
        + cap_note
    )
    return res


def _problem_worker(q, args, kwargs):
    """Child-process entry point: run one problem and ship the result dict back
    over the queue. Runs under the spawn start method, so everything here must be
    picklable (it is -- args are strings/ints, the result dict is plain data)."""
    try:
        res = run_problem(*args, **kwargs)
    except BaseException as e:  # never let the child die without reporting
        res = {
            "problem": args[0] if args else "?",
            "status": "worker-error",
            "error": f"{type(e).__name__}: {str(e)[:300]}",
        }
    try:
        q.put(res)
    except Exception:
        pass


def run_problem_isolated(
    folder, provider, api_key, model, rounds, hard_grace=30.0, **kwargs
):
    """Hard wall-clock cap: run run_problem in a child process and terminate it
    if it runs past problem_timeout + hard_grace.

    The child keeps all the cooperative (soft) deadline checks, so the common
    case finishes cleanly and returns partial/full results well before the kill.
    The kill is the backstop for the cases the cooperative deadline cannot
    interrupt: an in-process infinite loop in an LLM-generated validator /
    transform / relate / checker, or a hung LLM API call."""
    problem_timeout = kwargs.get("problem_timeout", 300.0)
    if not problem_timeout or problem_timeout <= 0:
        # No per-problem budget => no hard cap to enforce; run in-process.
        return run_problem(folder, provider, api_key, model, rounds, **kwargs)

    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    args = (folder, provider, api_key, model, rounds)
    proc = ctx.Process(target=_problem_worker, args=(q, args, kwargs), daemon=True)
    hard_deadline = problem_timeout + hard_grace
    t0 = time.time()
    proc.start()

    result = None
    try:
        # Returns as soon as the child posts its result (unblocking it), or
        # raises Empty at the hard deadline if the child is wedged.
        result = q.get(timeout=hard_deadline)
    except _queue.Empty:
        result = None
    except (EOFError, OSError):
        result = None

    # Brief join: a child that already posted its result exits within this window;
    # a wedged child won't, so we don't burn the full grace waiting on it again.
    proc.join(2)
    if proc.is_alive():
        elapsed = time.time() - t0
        print(
            f"  HARD CAP: terminating wedged problem after {elapsed:.0f}s "
            f"(> {hard_deadline:.0f}s budget+grace)"
        )
        proc.terminate()
        proc.join(5)
        if proc.is_alive():
            proc.kill()
            proc.join(5)

    if result is None:
        result = {
            "problem": folder,
            "status": "time-limit-exceeded",
            "stage": "hard-cap",
            "hard_killed": True,
            "time": time.time() - t0,
        }
    return result


def find_problems(difficulty=None, problem=None, min_difficulty=None, max_difficulty=None):
    if not os.path.isdir(DATA_DIR):
        raise FileNotFoundError(f"No {DATA_DIR}/ directory")
    if problem:
        for diff in sorted(os.listdir(DATA_DIR)):
            d = os.path.join(DATA_DIR, diff)
            if not os.path.isdir(d):
                continue
            p = os.path.join(d, problem)
            if os.path.isdir(p):
                return [p]
        raise FileNotFoundError(f"Problem {problem} not found under {DATA_DIR}/")
    problems = []
    for diff in sorted(os.listdir(DATA_DIR)):
        d = os.path.join(DATA_DIR, diff)
        if not os.path.isdir(d):
            continue
        if difficulty is not None and str(difficulty) not in diff:
            continue
        # Range filter (parsed difficulty number); buckets we can't parse are kept
        # only when no range is requested.
        if min_difficulty is not None or max_difficulty is not None:
            n = _extract_difficulty(d)
            if n is None:
                continue
            if min_difficulty is not None and n < min_difficulty:
                continue
            if max_difficulty is not None and n > max_difficulty:
                continue
        for p in sorted(os.listdir(d)):
            full = os.path.join(d, p)
            if os.path.isdir(full):
                problems.append(full)
    return problems


def summarize(results, model, provider, rounds):
    n = len(results)
    by_status = {}
    for r in results:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1

    exp_a = _aggregate_experiment_a(results)

    print("\n" + "=" * 72)
    print(f"SUMMARY  (provider={provider} model={model} rounds/relations={rounds})")
    print("=" * 72)
    print(f"Problems attempted: {n}")
    for s, c in sorted(by_status.items()):
        print(f"  {s:22s} {c}")

    if exp_a["relations"]:
        print(
            f"\nExperiment A (human submissions; per-relation over "
            f"{exp_a['relations']} generated relations):"
        )
        print(
            f"  AC false-positive rate:  {_pct(exp_a['ac_fp_rate'])}  "
            f"({exp_a['ac_flag']}/{exp_a['relations']} relations flagged a correct AC)"
        )
        print(
            f"  WA catch (per-relation): {_pct(exp_a['wa_pair_rate'])}  "
            f"({exp_a['wa_pair_flag']}/{exp_a['wa_pairs']})"
        )
        print(
            f"  WA catch (any relation): {_pct(exp_a['wa_union_rate'])}  "
            f"({exp_a['wa_union_caught']}/{exp_a['wa_union_total']})"
        )

    if any(r.get("goldens") for r in results):
        pop = _golden_population(results)
        pair = _golden_pair_confusion(results, "meta_samples_verdicts")
        union = _golden_union_confusion(results, "meta_samples_verdicts")
        print(f"\nExperiment B (golden eval, generated-samples variant):")
        print(
            f"  goldens:                {pop['gate_passed']}/{pop['generated']} passed gate; "
            f"wrong-answer={pop['wrong']} correct={pop['correct']} "
            f"slow={pop['slow']} unknown={pop['unknown']}"
        )
        print(
            f"  base rate wrong-answer: {_pct(pop['base_rate_wrong'])}  "
            f"(of decisive goldens; if ~0%, meta is redundant -- 'slow' are out of scope)"
        )
        print(
            f"  per-relation recall:    {_pct(pair['recall'])}  "
            f"(if ~0%, the meta check is useless)"
        )
        print(
            f"  per-relation FP rate:   {_pct(pair['fp_rate'])}  "
            f"(flagging a correct golden)"
        )
        print(
            f"  any-relation recall:    {_pct(union['recall'])}   "
            f"any-relation FP: {_pct(union['fp_rate'])}"
        )

    usage_agg = _aggregate_usage(results)
    if usage_agg["calls"]:
        print(f"\nAPI usage (this run, uncached calls only):")
        print(f"  total: {_fmt_usage(usage_agg)}")
        if usage_agg["problems"]:
            avg_tok = usage_agg["total_tokens"] / usage_agg["problems"]
            avg_cost = usage_agg["cost"] / usage_agg["problems"]
            print(
                f"  per problem (avg over {usage_agg['problems']}): "
                f"{avg_tok:.0f} tokens"
                + (f", ${avg_cost:.4f}" if usage_agg["cost"] else "")
            )
        capped = sum(1 for r in results if r.get("cost_limited"))
        if capped:
            print(f"  cost cap hit on {capped} problem(s)")

    return {
        "problems_attempted": n,
        "by_status": by_status,
        "exp_a": exp_a,
        "usage": usage_agg,
    }


def _md_escape(s):
    """Escape pipe + newline so a cell stays on one row in a markdown table."""
    if s is None:
        return ""
    return str(s).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def _extract_difficulty(problem_path):
    """Pull the difficulty number out of a path like
    Codeforces_Data/difficulty_2000/2195_F. Returns int or None."""
    if not problem_path:
        return None
    parts = problem_path.replace("\\", "/").split("/")
    for p in parts:
        if p.startswith("difficulty_"):
            try:
                return int(p.split("_", 1)[1])
            except (ValueError, IndexError):
                return None
    return None


def _aggregate_experiment_a(results):
    """Per-relation AC false-positive + WA catch across problems that produced
    relations. Each (relation x candidate) is one observation -- no AC filtering."""
    problems = relations = ac_flag = 0
    wa_pairs = wa_pair_flag = 0
    wa_union_total = wa_union_caught = 0
    for r in results:
        av = r.get("ac_verdicts")
        if av is None:
            continue
        problems += 1
        valid = [v for v in av if v in ("flag", "pass")]
        relations += len(valid)
        ac_flag += sum(1 for v in valid if v == "flag")
        for lst in (r.get("wa_verdicts") or {}).values():
            vs = [v for v in lst if v in ("flag", "pass")]
            wa_pairs += len(vs)
            wa_pair_flag += sum(1 for v in vs if v == "flag")
            if vs:
                wa_union_total += 1
                wa_union_caught += any(v == "flag" for v in vs)
    return {
        "problems": problems,
        "relations": relations,
        "ac_flag": ac_flag,
        "ac_fp_rate": (ac_flag / relations) if relations else None,
        "wa_pairs": wa_pairs,
        "wa_pair_flag": wa_pair_flag,
        "wa_pair_rate": (wa_pair_flag / wa_pairs) if wa_pairs else None,
        "wa_union_total": wa_union_total,
        "wa_union_caught": wa_union_caught,
        "wa_union_rate": (wa_union_caught / wa_union_total) if wa_union_total else None,
    }


def _aggregate_usage(results):
    """Sum per-problem API usage across all results."""
    agg = {
        "calls": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "cost": 0.0,
        "problems": 0,
    }
    for r in results:
        u = r.get("api_usage")
        if not u:
            continue
        agg["problems"] += 1
        for k in (
            "calls",
            "prompt_tokens",
            "completion_tokens",
            "total_tokens",
            "cost",
        ):
            agg[k] += u.get(k, 0)
    return agg


def _fmt_usage(u):
    """One-line usage string from a usage dict."""
    if not u or not u.get("calls"):
        return "0 calls"
    s = (
        f"{u['calls']} calls, {u.get('prompt_tokens', 0)}+{u.get('completion_tokens', 0)}"
        f"={u.get('total_tokens', 0)} tokens"
    )
    if u.get("cost"):
        s += f", ${u['cost']:.4f}"
    return s


def _pct(x):
    return f"{100 * x:.1f}%" if x is not None else "—"


def _confusion_table(conf):
    """Render one confusion matrix + derived rates as markdown lines."""
    L = []
    L.append("| | meta FLAGS | meta PASSES |")
    L.append("| --- | --- | --- |")
    L.append(f"| ground-truth WRONG | {conf['tp']} (TP) | {conf['fn']} (FN) |")
    L.append(f"| ground-truth CORRECT | {conf['fp']} (FP) | {conf['tn']} (TN) |")
    L.append("")
    L.append(f"- **Recall on wrong** `TP/(TP+FN)`: **{_pct(conf['recall'])}**")
    L.append(f"- False-positive rate `FP/(FP+TN)`: {_pct(conf['fp_rate'])}")
    L.append(f"- Observations scored: {conf['judged']}")
    return L


def _format_golden_section(results):
    """Markdown for experiment B. Returns [] if no problem ran goldens."""
    if not any(r.get("goldens") for r in results):
        return []
    pop = _golden_population(results)
    L = []
    L.append("## Golden-solution evaluation (experiment B)")
    L.append("")
    L.append(
        "Does a freshly generated metamorphic relation catch a *wrong LLM golden* "
        "that already passed compile + example I/O? Ground truth = differential testing "
        "vs the dataset `AC.txt`. A golden is **`wrong-answer`** only if it COMPLETED a run "
        "and the checker rejected it; one that times out is shrunk to a smaller input and, "
        "if it then agrees, classified **`slow`** (correct-but-too-slow / TLE) rather than "
        "wrong. **No AC-based filtering** — the metrics measure how a single generated "
        "relation behaves, exactly as the deployed workflow (which has no trusted reference) "
        "would use it."
    )
    L.append("")
    L.append(
        f"- **Goldens generated:** {pop['generated']}  "
        f"(**passed existing gate:** {pop['gate_passed']})"
    )
    L.append(
        f"- **Ground truth (gate-pass):** {pop['wrong']} wrong-answer, "
        f"{pop['correct']} correct, {pop['slow']} slow (TLE), {pop['unknown']} unknown"
    )
    L.append(
        f"- **Base rate wrong-answer** (of decisive goldens = wrong-answer + correct): "
        f"**{_pct(pop['base_rate_wrong'])}** — if ~0%, the check is redundant here. "
        f"`slow` goldens are out of the metamorphic check's scope (the stress tester "
        f"detects a slow reference itself) and are excluded from the confusion matrix."
    )
    L.append("")
    for variant_key, vlabel in (
        ("meta_samples_verdicts", "Generated-samples variant (strong)"),
        (
            "meta_example_verdicts",
            "Example-only variant (faithful to current AC_generator wiring)",
        ),
    ):
        pair = _golden_pair_confusion(results, variant_key)
        union = _golden_union_confusion(results, variant_key)
        L.append(f"### {vlabel}")
        L.append("")
        L.append(
            "**Per-relation** (each relation × golden is one trial — the realistic headline):"
        )
        L.append("")
        L.extend(_confusion_table(pair))
        L.append("")
        L.append(
            f"**Any-relation union** (best of the R relations): "
            f"recall {_pct(union['recall'])}, FP {_pct(union['fp_rate'])}"
        )
        L.append("")

    # Per-difficulty recall/base-rate (strong variant, per-relation) -- the key curve.
    buckets = {}
    for r in results:
        if not r.get("goldens"):
            continue
        diff = _extract_difficulty(r.get("problem", ""))
        buckets.setdefault(diff, []).append(r)
    if buckets:
        L.append("### Per difficulty (generated-samples, per-relation)")
        L.append("")
        L.append("| Difficulty | Gate-pass | Base-rate wrong | Recall | FP rate |")
        L.append("| --- | --- | --- | --- | --- |")
        for diff in sorted(
            buckets.keys(), key=lambda d: (d is None, d if d is not None else 0)
        ):
            sub_pop = _golden_population(buckets[diff])
            sub_pair = _golden_pair_confusion(buckets[diff], "meta_samples_verdicts")
            label = str(diff) if diff is not None else "(unknown)"
            L.append(
                f"| {label} | {sub_pop['gate_passed']} | {_pct(sub_pop['base_rate_wrong'])} | "
                f"{_pct(sub_pair['recall'])} | {_pct(sub_pair['fp_rate'])} |"
            )
        L.append("")
    return L


def _format_golden_per_problem(gr):
    """Markdown detail for one problem's golden corpus. gr is the 'goldens' dict.
    The two verdict columns show how many of the R relations flagged each golden."""
    L = []
    L.append(
        f"**Goldens:** {gr.get('gate_passed', 0)} / {gr.get('num_goldens', 0)} passed gate"
    )
    L.append("")
    corpus = gr.get("corpus") or []
    if corpus:
        L.append(
            "| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |"
        )
        L.append("| --- | --- | --- | --- | --- | --- |")
        for g in corpus:
            ex = g.get("meta_example_verdicts") or []
            sm = g.get("meta_samples_verdicts") or []
            ex_s = f"{sum(1 for v in ex if v == 'flag')} / {len(ex)}" if ex else "—"
            sm_s = f"{sum(1 for v in sm if v == 'flag')} / {len(sm)}" if sm else "—"
            note = g.get("gt_witness") or g.get("gate_reason") or ""
            L.append(
                f"| {g.get('index', '?')} | `{g.get('gate', '?')}` | "
                f"`{g.get('ground_truth', '—')}` | {ex_s} | {sm_s} | {_md_escape(note)[:140]} |"
            )
        L.append("")
    return L


def _format_markdown(provider, model, rounds, samples_per_round, agg, results):
    L = []
    L.append("# Metamorphic Benchmark Results")
    L.append("")
    L.append(f"- **Provider:** {provider}")
    L.append(f"- **Model:** `{model}`")
    L.append(f"- **Relations per problem (R = rounds):** {rounds}")
    L.append(f"- **Samples per relation (S):** {samples_per_round}")
    L.append("")

    exp_a = agg.get("exp_a") or _aggregate_experiment_a(results)
    L.append("## Aggregate")
    L.append("")
    L.append(
        "Experiment A measures the metamorphic relation on human submissions, "
        "**per generated relation** (each of the R relations is one independent trial)."
    )
    L.append("")
    L.append("| Metric | Value |")
    L.append("| --- | --- |")
    L.append(f"| Problems attempted | {agg['problems_attempted']} |")
    L.append(f"| Problems that produced relations | {exp_a['problems']} |")
    L.append(f"| Relations generated (valid) | {exp_a['relations']} |")
    L.append(
        f"| **AC false-positive rate** (per-relation) | "
        f"**{exp_a['ac_flag']} / {exp_a['relations']} ({_pct(exp_a['ac_fp_rate'])})** |"
    )
    L.append(
        f"| WA catch rate (per-relation) | "
        f"{exp_a['wa_pair_flag']} / {exp_a['wa_pairs']} ({_pct(exp_a['wa_pair_rate'])}) |"
    )
    L.append(
        f"| WA catch rate (any relation) | "
        f"{exp_a['wa_union_caught']} / {exp_a['wa_union_total']} ({_pct(exp_a['wa_union_rate'])}) |"
    )
    usage_agg = _aggregate_usage(results)
    if usage_agg["calls"]:
        L.append(f"| API calls (this run, uncached) | {usage_agg['calls']} |")
        L.append(
            f"| API tokens (prompt + completion) | "
            f"{usage_agg['prompt_tokens']} + {usage_agg['completion_tokens']} "
            f"= {usage_agg['total_tokens']} |"
        )
        if usage_agg["cost"]:
            L.append(f"| **API cost (this run)** | **${usage_agg['cost']:.4f}** |")
    L.append("")

    if agg.get("by_status"):
        L.append("### Problem status breakdown")
        L.append("")
        L.append("| Status | Count |")
        L.append("| --- | --- |")
        for s, c in sorted(agg["by_status"].items()):
            L.append(f"| `{s}` | {c} |")
        L.append("")

    L.extend(_format_golden_section(results))

    buckets = {}
    for r in results:
        diff = _extract_difficulty(r.get("problem", ""))
        buckets.setdefault(diff, []).append(r)
    bucket_keys = sorted(
        buckets.keys(), key=lambda d: (d is None, d if d is not None else 0)
    )

    if len(buckets) > 1 or (buckets and next(iter(buckets)) is not None):
        L.append("## Per difficulty (experiment A)")
        L.append("")
        L.append(
            "| Difficulty | Problems | Relations | AC-FP rate | WA catch (per-rel) | WA catch (union) |"
        )
        L.append("| --- | --- | --- | --- | --- | --- |")
        for diff in bucket_keys:
            sub = _aggregate_experiment_a(buckets[diff])
            diff_label = str(diff) if diff is not None else "(unknown)"
            L.append(
                f"| {diff_label} | {len(buckets[diff])} | {sub['relations']} | "
                f"{_pct(sub['ac_fp_rate'])} | {_pct(sub['wa_pair_rate'])} | "
                f"{_pct(sub['wa_union_rate'])} |"
            )
        L.append("")

    L.append("## Per problem")
    L.append("")
    ordered_results = [r for diff in bucket_keys for r in buckets[diff]]
    for r in ordered_results:
        problem = r.get("problem", "?")
        status = r.get("status", "?")
        t = r.get("time")
        time_str = f"{t:.1f}s" if isinstance(t, (int, float)) else "?"
        L.append(f"### `{problem}`")
        L.append("")
        L.append(f"**Status:** `{status}`  **Time:** {time_str}")
        if r.get("api_usage") and r["api_usage"].get("calls"):
            L.append("")
            cap = "  ⚠️ **cost cap hit**" if r.get("cost_limited") else ""
            L.append(f"**API usage (this run):** {_fmt_usage(r['api_usage'])}{cap}")
        L.append("")

        if "ac_verdicts" in r:
            valid = r.get("relations_valid", 0)
            req = r.get("relations_requested", 0)
            extra = []
            if r.get("relations_declined"):
                extra.append(f"{r['relations_declined']} declined")
            if r.get("relations_errored"):
                extra.append(f"{r['relations_errored']} errored")
            extra_s = f" ({', '.join(extra)})" if extra else ""
            L.append(f"**Relations:** {valid} valid / {req} requested{extra_s}")
            L.append("")

            ac_fp = r.get("ac_fp_count", 0)
            L.append(
                f"**AC false-positive:** {ac_fp} / {valid} relations flagged the human AC"
            )
            if ac_fp and r.get("ac_fp_reason"):
                L.append("")
                L.append(
                    f"> **AC-FP sample reason:** {_md_escape(r['ac_fp_reason'])[:200]}"
                )
            L.append("")

            wa_verdicts = r.get("wa_verdicts") or {}
            wa_reasons = r.get("wa_reasons") or {}
            if wa_verdicts:
                L.append("| WA | Caught by / relations | Rate | Reason |")
                L.append("| --- | --- | --- | --- |")
                for label in sorted(wa_verdicts.keys()):
                    vs = [v for v in wa_verdicts[label] if v in ("flag", "pass")]
                    flagged = sum(1 for v in vs if v == "flag")
                    rate = _pct(flagged / len(vs)) if vs else "—"
                    reason_md = _md_escape(wa_reasons.get(label, ""))[:200]
                    L.append(
                        f"| {label} | {flagged} / {len(vs)} | {rate} | {reason_md} |"
                    )
                L.append("")

            gr = r.get("goldens")
            if gr:
                L.extend(_format_golden_per_problem(gr))
        else:
            if status == "time-limit-exceeded" and r.get("stage"):
                L.append(
                    f"**Time limit exceeded** during `{r['stage']}` (no relation results)."
                )
                L.append("")
            err_lines = []
            if r.get("error"):
                err_lines.append(_md_escape(r["error"]))
            if r.get("relation_failures"):
                for f in r["relation_failures"]:
                    err_lines.append(
                        f"round {f.get('round', '?')} ({f.get('stage', '?')}): "
                        f"{_md_escape(f.get('error', ''))}"
                    )
            if r.get("compile_errors"):
                for label, err in r["compile_errors"].items():
                    err_lines.append(f"{label} compile error: {_md_escape(err)}")
            for line in err_lines[:8]:
                L.append(f"- {line}")
            if err_lines:
                L.append("")
            # A TLE problem may still have a partial golden corpus.
            gr = r.get("goldens")
            if gr:
                L.extend(_format_golden_per_problem(gr))

    return "\n".join(L) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--difficulty",
        type=int,
        default=None,
        help="Limit to one difficulty bucket (e.g. 2000)",
    )
    parser.add_argument(
        "--problem",
        type=str,
        default=None,
        help="Single problem folder name (e.g. 2217_E)",
    )
    parser.add_argument(
        "--min-difficulty",
        type=int,
        default=None,
        help="Only run difficulty buckets >= this (e.g. 2200 to skip 2000/2100). "
        "Combine with --max-difficulty for a range. Honored with or without --run-all.",
    )
    parser.add_argument(
        "--max-difficulty",
        type=int,
        default=None,
        help="Only run difficulty buckets <= this.",
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run every problem in every difficulty bucket (subject to "
        "--min-difficulty / --max-difficulty). Overrides --difficulty / --problem.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="R = number of INDEPENDENT metamorphic relations generated per "
        "problem (default 5). Each relation is a fresh LLM generation and "
        "is scored separately, so this measures relation-to-relation "
        "reliability. Costs R metamorphic generations per problem.",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=1,
        help="Within a single relation round, retry generation up to N times "
        "if it errors or the LLM declines (default 1). Does not add "
        "independent relations -- use --rounds for that.",
    )
    parser.add_argument(
        "--out", type=str, default="benchmark_results.md", help="Output markdown path"
    )
    parser.add_argument(
        "--json-out",
        type=str,
        default=None,
        help="Also dump the raw results list as JSON, for combining runs across "
        "difficulty bands with tests/results_io.py.",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default=None,
        choices=["Gemini", "Claude", "OpenAI", "OpenRouter", "vLLM"],
        help="Override provider (else uses settings.yaml Last_Use / env vars)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Override model id (e.g. 'anthropic/claude-sonnet-4' for OpenRouter)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore and overwrite the on-disk validator/generator cache",
    )
    parser.add_argument(
        "--no-generator",
        action="store_true",
        help="Skip the random testcase generator; only run metamorphic rounds "
        "on the statement's example input (faster, weaker)",
    )
    parser.add_argument(
        "--samples-per-round",
        type=int,
        default=10,
        help="When the generator is enabled, how many random inputs to draw "
        "and test per round (default 10). Total tests per candidate is "
        "rounds * samples_per_round.",
    )
    parser.add_argument(
        "--problem-timeout",
        type=float,
        default=300.0,
        help="Wall-clock seconds budget per problem (default 300). "
        "If exceeded the problem is reported as 'time-limit-exceeded' "
        "with whatever partial results were collected. Pass 0 to disable.",
    )
    parser.add_argument(
        "--goldens",
        type=int,
        default=0,
        help="Golden-solution evaluation (experiment B): generate this many "
        "first-edition LLM goldens per problem, label each against the "
        "dataset AC.txt, and score the metamorphic relation as an "
        "incremental gate. 0 (default) skips experiment B entirely.",
    )
    parser.add_argument(
        "--golden-label-inputs",
        type=int,
        default=20,
        help="When --goldens > 0, how many generator inputs to differential-test "
        "each golden against AC.txt for ground-truth labeling (default 20).",
    )
    parser.add_argument(
        "--gen-workers",
        type=int,
        default=2,
        help="Parallel threads for independent LLM generations per problem "
        "(default 2): both the K goldens and the R metamorphic relations are "
        "generated concurrently. Raise to overlap latency, but mind your "
        "provider's rate limit. Scoring / gating / labeling stay sequential "
        "(they spawn CPU-bound subprocesses).",
    )
    parser.add_argument(
        "--cost-cap",
        type=float,
        default=1.0,
        help="Hard per-problem USD cost cap (default 1.0). Once a problem's API "
        "spend reaches this, every further LLM call is blocked at the source, so "
        "one pathological problem can't burn $6. Overshoot is bounded by the calls "
        "in flight when the cap is crossed (lower --gen-workers to tighten it). "
        "Pass 0 to disable. Effective for OpenRouter (reported cost) and Claude "
        "(cost estimated from a per-model price table in utils/claude.py).",
    )
    parser.add_argument(
        "--max-call-cost",
        type=float,
        default=1.0,
        help="Per-SINGLE-call USD ceiling (default 1.0). Before each LLM call the "
        "agent estimates its worst-case cost (input tokens + full max_tokens of "
        "output) and refuses the call if it would exceed this -- a guard against one "
        "runaway call even when the cumulative --cost-cap still has room. Output is "
        "also hard-bounded by max_tokens (8192). Pass 0 to disable. (Claude only; "
        "OpenRouter has no pre-call price table but its output is max_tokens-bounded.)",
    )
    parser.add_argument(
        "--no-isolate",
        action="store_true",
        help="Run each problem in-process instead of in a child process. "
        "Faster (no spawn overhead) but loses the HARD wall-clock cap: "
        "an in-process infinite loop or hung LLM call could overshoot "
        "--problem-timeout. Cooperative (soft) checks still apply.",
    )
    parser.add_argument(
        "--hard-grace",
        type=float,
        default=30.0,
        help="Extra seconds past --problem-timeout before a problem's child "
        "process is force-killed (default 30). The grace lets the soft "
        "deadline stop cleanly and record partial results first.",
    )
    args = parser.parse_args()

    provider, api_key, model = load_credentials(
        provider_override=args.provider, model_override=args.model
    )
    if not api_key:
        scope = f" for provider '{args.provider}'" if args.provider else ""
        print(
            f"No API key found{scope}. Set the relevant env var or update Input_Cache/settings.yaml."
        )
        return 1
    print(f"provider={provider} model={model} rounds={args.rounds}")

    cleanup_tmp_storage()

    if args.run_all:
        if args.difficulty is not None or args.problem is not None:
            print("note: --run-all is set; ignoring --difficulty / --problem filters")
        problems = find_problems(
            difficulty=None, problem=None,
            min_difficulty=args.min_difficulty, max_difficulty=args.max_difficulty,
        )
    else:
        problems = find_problems(
            difficulty=args.difficulty, problem=args.problem,
            min_difficulty=args.min_difficulty, max_difficulty=args.max_difficulty,
        )
    diffs_found = sorted({_extract_difficulty(p) for p in problems} - {None})
    diff_str = ", ".join(str(d) for d in diffs_found) if diffs_found else "—"
    print(f"Found {len(problems)} problem(s) across difficulties: {diff_str}")

    results = []
    bench_start = time.time()
    total = len(problems)
    for i, folder in enumerate(problems, 1):
        elapsed = time.time() - bench_start
        progress_bits = [f"[{i}/{total}]"]
        if i > 1:
            avg = elapsed / (i - 1)
            remaining = (total - i + 1) * avg
            progress_bits.append(
                f"(elapsed {elapsed/60:.1f}m, ETA ~{remaining/60:.1f}m)"
            )
        print(f"\n=== {' '.join(progress_bits)} {folder} ===")
        try:
            runner = run_problem if args.no_isolate else run_problem_isolated
            extra = {} if args.no_isolate else {"hard_grace": args.hard_grace}
            r = runner(
                folder,
                provider,
                api_key,
                model,
                args.rounds,
                attempts=args.attempts,
                use_cache=not args.no_cache,
                use_generator=not args.no_generator,
                samples_per_round=args.samples_per_round,
                problem_timeout=args.problem_timeout,
                num_goldens=args.goldens,
                label_inputs=args.golden_label_inputs,
                gen_workers=args.gen_workers,
                cost_cap=(args.cost_cap if args.cost_cap and args.cost_cap > 0 else None),
                call_cap=(args.max_call_cost if args.max_call_cost and args.max_call_cost > 0 else None),
                **extra,
            )
            results.append(r)
            # Running-total summary so the user sees aggregate progress as it grows.
            ok_count = sum(1 for x in results if x.get("status") == "ok")
            tle_count = sum(
                1 for x in results if x.get("status") == "time-limit-exceeded"
            )
            wa_total = sum(
                x.get("wa_total", 0) for x in results if x.get("status") == "ok"
            )
            wa_caught = sum(
                x.get("wa_caught", 0) for x in results if x.get("status") == "ok"
            )
            wa_pct = f"{100*wa_caught/wa_total:.0f}%" if wa_total else "n/a"
            print(
                f"  --> running totals: ok={ok_count}  tle={tle_count}  "
                f"WA catch={wa_caught}/{wa_total} ({wa_pct})"
            )
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        except Exception as e:
            import traceback

            traceback.print_exc()
            results.append(
                {"problem": folder, "status": "unhandled-error", "error": str(e)[:300]}
            )

    agg = summarize(results, model, provider, args.rounds)

    md = _format_markdown(
        provider, model, args.rounds, args.samples_per_round, agg, results
    )
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"\nWrote detailed results to {args.out}")
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=1)
        print(f"Wrote raw results JSON to {args.json_out} "
              f"(combine across runs with tests/results_io.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
