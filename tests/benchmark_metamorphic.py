"""
Benchmark Metamorphic_Agent across the Codeforces_Data/ corpus.

For each problem:
  - parse statement + first example I/O
  - generate validator + metamorphic relation
  - measure AC false-positive rate: does the AC code pass the metamorphic check?
  - measure WA catch rate: of WA codes, what fraction does the metamorphic check flag?
    Each code is tested over N independent metamorphic rounds (the transform is
    randomized, so repetition meaningfully increases sensitivity). A WA is flagged
    if *any* of its rounds catches it.

Layout expected:
  Codeforces_Data/difficulty_<N>/<contest>_<problem>/
    statement.txt or statement.md
    AC.txt
    WA1.txt, WA2.txt, ...

Usage:
  python -m tests.benchmark_metamorphic [--difficulty 2000] [--problem 2217_E]
                                        [--rounds 5] [--out benchmark_results.json]
"""

import argparse
import json
import os
import re
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from utils.code import Code
from utils.agent import Agent
from utils.signal import Signal_Queue
from scripts.validator import TC_Validator_Agent
from scripts.metamorphic import Metamorphic_Agent
from scripts.AC_generator import AC_Agent
from tests.integration_metamorphic import load_credentials

DATA_DIR = "Codeforces_Data"
TMP_DIR = "tmp_storage"


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
    for name in ('statement.txt', 'statement.md'):
        p = os.path.join(folder, name)
        if os.path.exists(p):
            statement_path = p
            break
    if not statement_path:
        raise FileNotFoundError(f"No statement.{{txt,md}} in {folder}")
    with open(statement_path, encoding='utf-8') as f:
        statement = f.read()

    in_match = _INPUT_BLOCK_RE.search(statement)
    out_match = _OUTPUT_BLOCK_RE.search(statement)
    if not in_match or not out_match:
        raise ValueError(f"Could not extract first example I/O from {statement_path}")
    example_in = in_match.group(1).rstrip() + "\n"
    example_out = out_match.group(1).rstrip() + "\n"

    ac_path = os.path.join(folder, 'AC.txt')
    if not os.path.exists(ac_path):
        raise FileNotFoundError(f"Missing AC.txt in {folder}")
    with open(ac_path, encoding='utf-8') as f:
        ac_text = f.read()

    wa_texts = []
    for fname in sorted(os.listdir(folder)):
        if re.fullmatch(r'WA\d+\.txt', fname):
            with open(os.path.join(folder, fname), encoding='utf-8') as f:
                wa_texts.append((fname[:-4], f.read()))

    return statement, example_in, example_out, ac_text, wa_texts


def test_code(code_text, statement, example_in, example_out, meta, rounds):
    try:
        code = Code(code_text)
    except Exception as e:
        return {'status': 'compile-error', 'detail': str(e)[:300]}

    run = code.execute(example_in, timeout=15)
    if run == 'timeout':
        return {'status': 'exec-timeout'}
    if getattr(run, 'stderr', '') or getattr(run, 'returncode', 0) != 0:
        return {'status': 'exec-error', 'detail': (getattr(run, 'stderr', '') or '')[:300]}

    original_stdout = run.stdout

    ac_agent = AC_Agent(None, statement, example_in, example_out)
    ac_agent.AC_code = code
    ac_agent.set_metamorphic(meta)

    reasons = []
    for _ in range(rounds):
        r = ac_agent._metamorphic_check(original_stdout)
        if r is not None:
            reasons.append(r[:200])

    if reasons:
        return {'status': 'caught', 'rounds_caught': len(reasons),
                'rounds_total': rounds, 'sample_reason': reasons[0]}
    return {'status': 'pass', 'rounds_total': rounds}


def _generate_metamorphic(provider, api_key, model, statement, example_in, example_out):
    """One attempt: build validator, then metamorphic relation.
    Returns (meta, failure_dict). On success, failure_dict is None and meta is non-None.
    On failure or LLM decline, meta is None and failure_dict describes why.
    """
    sq = Signal_Queue()
    try:
        val_agent = Agent(sq, provider, api_key, model, "Validator")
        validator = TC_Validator_Agent(val_agent, statement, example_in, example_out).work()
    except Exception as e:
        print(f"  validator gen failed: {e}")
        return None, {'stage': 'validator', 'error': str(e)[:300]}
    try:
        meta_agent = Agent(sq, provider, api_key, model, "Metamorphic")
        meta = Metamorphic_Agent(meta_agent, statement, example_in, example_out).generate(validator)
    except Exception as e:
        print(f"  metamorphic gen failed: {e}")
        return None, {'stage': 'metamorphic', 'error': str(e)[:300]}
    if meta is None:
        print("  LLM declined to provide a metamorphic relation")
        return None, {'stage': 'declined'}
    return meta, None


def _run_problem_inner(folder, provider, api_key, model, rounds, attempts):
    t0 = time.time()
    try:
        statement, example_in, example_out, ac_text, wa_texts = parse_problem(folder)
    except Exception as e:
        print(f"  parse failed: {e}")
        return {'problem': folder, 'status': 'parse-error', 'error': str(e)}

    failures = []
    meta = None
    successful_attempt = None
    for attempt in range(1, attempts + 1):
        if attempts > 1:
            print(f"  -- attempt {attempt}/{attempts} --")
        meta, failure = _generate_metamorphic(provider, api_key, model,
                                               statement, example_in, example_out)
        if meta is not None:
            successful_attempt = attempt
            break
        failures.append({'attempt': attempt, **failure})

    if meta is None:
        last_stage = failures[-1]['stage'] if failures else 'unknown'
        status_map = {'validator': 'validator-error',
                      'metamorphic': 'metamorphic-error',
                      'declined': 'declined'}
        return {'problem': folder,
                'status': status_map.get(last_stage, 'failed'),
                'attempts_tried': len(failures),
                'failures': failures,
                'time': time.time() - t0}

    ac_result = test_code(ac_text, statement, example_in, example_out, meta, rounds)
    wa_results = {}
    for label, text in wa_texts:
        wa_results[label] = test_code(text, statement, example_in, example_out, meta, rounds)

    wa_total = len(wa_results)
    wa_caught = sum(1 for v in wa_results.values() if v['status'] == 'caught')

    print(f"  AC: {ac_result['status']}"
          + (f" (oops, false positive in {ac_result.get('rounds_caught')} / {ac_result.get('rounds_total')} rounds)"
             if ac_result['status'] == 'caught' else ''))
    for label, v in wa_results.items():
        if v['status'] == 'caught':
            print(f"  {label}: caught ({v['rounds_caught']}/{v['rounds_total']} rounds)")
        else:
            print(f"  {label}: {v['status']}")
    print(f"  WA catch rate: {wa_caught}/{wa_total}"
          + (f" = {100*wa_caught/wa_total:.0f}%" if wa_total else ""))

    return {
        'problem': folder,
        'status': 'ok',
        'attempt_succeeded': successful_attempt,
        'attempts_tried': successful_attempt,
        'prior_failures': failures,
        'time': time.time() - t0,
        'ac': ac_result,
        'wa': wa_results,
        'wa_caught': wa_caught,
        'wa_total': wa_total,
    }


def run_problem(folder, provider, api_key, model, rounds, attempts=1):
    print(f"\n=== {folder} ===")
    try:
        return _run_problem_inner(folder, provider, api_key, model, rounds, attempts)
    finally:
        cleanup_tmp_storage()


def find_problems(difficulty=None, problem=None):
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
        if difficulty is not None and str(difficulty) not in diff:
            continue
        d = os.path.join(DATA_DIR, diff)
        if not os.path.isdir(d):
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
        by_status[r['status']] = by_status.get(r['status'], 0) + 1

    ok = [r for r in results if r.get('status') == 'ok']
    ac_pass = sum(1 for r in ok if r['ac']['status'] == 'pass')
    ac_false_pos = sum(1 for r in ok if r['ac']['status'] == 'caught')
    ac_other = sum(1 for r in ok if r['ac']['status'] not in ('pass', 'caught'))
    wa_total = sum(r['wa_total'] for r in ok)
    wa_caught = sum(r['wa_caught'] for r in ok)

    print("\n" + "=" * 72)
    print(f"SUMMARY  (provider={provider} model={model} rounds={rounds})")
    print("=" * 72)
    print(f"Problems attempted: {n}")
    for s, c in sorted(by_status.items()):
        print(f"  {s:20s} {c}")
    ac_executed = ac_pass + ac_false_pos
    if ok:
        if ac_executed:
            print(f"\nAC success rate:      {ac_pass}/{ac_executed} "
                  f"({100*ac_pass/ac_executed:.1f}%) "
                  f"(of AC codes that actually ran)")
        print(f"  AC passed cleanly:    {ac_pass}")
        print(f"  AC caught (false +):  {ac_false_pos}")
        print(f"  AC compile/exec err:  {ac_other}")
    if wa_total:
        print(f"\nWA catch rate:        {wa_caught}/{wa_total} "
              f"({100*wa_caught/wa_total:.1f}%)")

    return {
        'problems_attempted': n,
        'by_status': by_status,
        'ok_problems': len(ok),
        'ac_pass': ac_pass,
        'ac_false_positive': ac_false_pos,
        'ac_other': ac_other,
        'ac_executed': ac_executed,
        'ac_success_rate': (ac_pass / ac_executed) if ac_executed else None,
        'wa_total': wa_total,
        'wa_caught': wa_caught,
        'wa_catch_rate': (wa_caught / wa_total) if wa_total else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', type=int, default=None,
                        help="Limit to one difficulty bucket (e.g. 2000)")
    parser.add_argument('--problem', type=str, default=None,
                        help="Single problem folder name (e.g. 2217_E)")
    parser.add_argument('--rounds', type=int, default=5,
                        help="Independent metamorphic rounds per code (default 5)")
    parser.add_argument('--attempts', type=int, default=1,
                        help="Retry validator+metamorphic generation up to N times per problem "
                             "if it errors or the LLM declines (default 1, fresh agents per attempt)")
    parser.add_argument('--out', type=str, default='benchmark_results.json',
                        help="Output JSON path")
    parser.add_argument('--provider', type=str, default=None,
                        choices=['Gemini', 'Claude', 'OpenAI', 'OpenRouter', 'vLLM'],
                        help="Override provider (else uses settings.yaml Last_Use / env vars)")
    parser.add_argument('--model', type=str, default=None,
                        help="Override model id (e.g. 'anthropic/claude-sonnet-4' for OpenRouter)")
    args = parser.parse_args()

    provider, api_key, model = load_credentials(provider_override=args.provider,
                                                model_override=args.model)
    if not api_key:
        scope = f" for provider '{args.provider}'" if args.provider else ""
        print(f"No API key found{scope}. Set the relevant env var or update Input_Cache/settings.yaml.")
        return 1
    print(f"provider={provider} model={model} rounds={args.rounds}")

    cleanup_tmp_storage()

    problems = find_problems(difficulty=args.difficulty, problem=args.problem)
    print(f"Found {len(problems)} problem(s)")

    results = []
    for folder in problems:
        try:
            results.append(run_problem(folder, provider, api_key, model,
                                       args.rounds, attempts=args.attempts))
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break
        except Exception as e:
            import traceback
            traceback.print_exc()
            results.append({'problem': folder, 'status': 'unhandled-error',
                            'error': str(e)[:300]})

    agg = summarize(results, model, provider, args.rounds)

    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump({
            'provider': provider,
            'model': model,
            'rounds': args.rounds,
            'aggregate': agg,
            'per_problem': results,
        }, f, indent=2, default=str)
    print(f"\nWrote detailed results to {args.out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
