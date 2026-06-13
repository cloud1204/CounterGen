"""Read/relabel/merge benchmark result sets.

The benchmark only ever wrote rendered markdown, so the raw per-problem data of an
already-finished run lives only in that markdown. This module:

  - parses a benchmark_results.md back into a results list (the same dicts the
    benchmark builds in memory),
  - optionally relabels timed-out 'wrong' goldens as 'slow' (the shrink+split
    semantics, applied retroactively to a pre-split run),
  - writes a combinable JSON and/or re-renders the corrected markdown,
  - merges several result JSONs into one combined report.

Usage:
  # Correct an old run and save JSON + corrected markdown:
  python -m tests.results_io --parse benchmark_results.md --relabel-timeouts \
      --json-out results_2000-2100.json --md-out results_2000-2100.md

  # Later, combine with a fresh run that used `--json-out results_2200plus.json`:
  python -m tests.results_io --merge results_2000-2100.json results_2200plus.json \
      --md-out combined.md
"""
import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from tests.benchmark_metamorphic import (  # noqa: E402
    _aggregate_experiment_a,
    _format_markdown,
)


def _verdicts(flagged, total):
    """Reconstruct a verdict list of `total` entries with `flagged` flags. Order
    is irrelevant to every downstream metric (they all just count)."""
    flagged = max(0, min(flagged, total))
    return ["flag"] * flagged + ["pass"] * (total - flagged)


def _relabel_ground_truth(old, note):
    """Map an old pre-split label to the new vocabulary. A 'wrong' golden whose
    note shows it timed out (or has no decisive mismatch) becomes 'slow'; a clear
    output mismatch stays 'wrong-answer'."""
    if old == "correct":
        return "correct"
    if old == "wrong":
        n = (note or "").lower()
        if "timed out" in n or "timeout" in n or "tle" in n:
            return "slow"
        if "mismatch" in n or "expected" in n or "got " in n or "vs " in n:
            return "wrong-answer"
        return "slow"  # default per the observed all-TLE distribution
    return old


_RE_HEADER_MODEL = re.compile(r"^- \*\*Model:\*\* `([^`]+)`")
_RE_HEADER_PROVIDER = re.compile(r"^- \*\*Provider:\*\* (.+)")
_RE_HEADER_R = re.compile(r"^- \*\*Relations per problem \(R = rounds\):\*\* (\d+)")
_RE_HEADER_S = re.compile(r"^- \*\*Samples per relation \(S\):\*\* (\d+)")
_RE_PROBLEM = re.compile(r"^### `([^`]+)`")
_RE_STATUS = re.compile(r"^\*\*Status:\*\* `([^`]+)`\s+\*\*Time:\*\* ([\d.]+)s")
_RE_USAGE = re.compile(
    r"^\*\*API usage \(this run\):\*\* (\d+) calls, (\d+)\+(\d+)=(\d+) tokens(?:, \$([\d.]+))?"
)
_RE_RELATIONS = re.compile(r"^\*\*Relations:\*\* (\d+) valid / (\d+) requested")
_RE_ACFP = re.compile(r"^\*\*AC false-positive:\*\* (\d+) / (\d+) relations")
_RE_GOLDENS = re.compile(r"^\*\*Goldens:\*\* (\d+) / (\d+) passed gate")
_RE_FRAC = re.compile(r"(\d+)\s*/\s*(\d+)")


def _split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_markdown(path):
    """Parse a benchmark markdown report into (header, results)."""
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    header = {"provider": "unknown", "model": "unknown", "rounds": 0, "samples": 0}
    for line in lines[:20]:
        for rx, key, cast in (
            (_RE_HEADER_PROVIDER, "provider", str),
            (_RE_HEADER_MODEL, "model", str),
            (_RE_HEADER_R, "rounds", int),
            (_RE_HEADER_S, "samples", int),
        ):
            m = rx.match(line)
            if m:
                header[key] = cast(m.group(1))

    # Slice out the per-problem section.
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "## Per problem")
    except StopIteration:
        return header, []

    results = []
    cur = None
    table = None  # 'wa' | 'golden' | None
    for line in lines[start + 1:]:
        mp = _RE_PROBLEM.match(line)
        if mp:
            if cur is not None:
                results.append(_finalize(cur))
            cur = {"problem": mp.group(1), "wa_rows": [], "golden_rows": []}
            table = None
            continue
        if cur is None:
            continue

        m = _RE_STATUS.match(line)
        if m:
            cur["status"] = m.group(1)
            cur["time"] = float(m.group(2))
            continue
        m = _RE_USAGE.match(line)
        if m:
            cur["api_usage"] = {
                "calls": int(m.group(1)),
                "prompt_tokens": int(m.group(2)),
                "completion_tokens": int(m.group(3)),
                "total_tokens": int(m.group(4)),
                "cost": float(m.group(5)) if m.group(5) else 0.0,
            }
            cur["cost_limited"] = "cost cap hit" in line
            continue
        m = _RE_RELATIONS.match(line)
        if m:
            cur["relations_valid"] = int(m.group(1))
            cur["relations_requested"] = int(m.group(2))
            continue
        m = _RE_ACFP.match(line)
        if m:
            cur["ac_fp_count"] = int(m.group(1))
            cur["ac_relations"] = int(m.group(2))
            continue
        m = _RE_GOLDENS.match(line)
        if m:
            cur["gate_passed"] = int(m.group(1))
            cur["num_goldens"] = int(m.group(2))
            continue

        if line.startswith("|"):
            cells = _split_row(line)
            if cells and cells[0] in ("WA", "#") or set("".join(cells)) <= set("- "):
                table = "wa" if cells and cells[0] == "WA" else (
                    "golden" if cells and cells[0] == "#" else table
                )
                continue  # header / separator row
            if table == "wa" and len(cells) >= 4:
                cur["wa_rows"].append(cells)
            elif table == "golden" and len(cells) >= 6:
                cur["golden_rows"].append(cells)
            continue
        if line.strip() == "":
            table = None

    if cur is not None:
        results.append(_finalize(cur))
    return header, results


def _finalize(cur):
    """Turn the scratch parse dict into a benchmark-shaped result dict."""
    r = {"problem": cur["problem"], "status": cur.get("status", "?")}
    if "time" in cur:
        r["time"] = cur["time"]
    if "api_usage" in cur:
        r["api_usage"] = cur["api_usage"]
        r["cost_limited"] = cur.get("cost_limited", False)

    if "relations_valid" in cur:
        v = cur["relations_valid"]
        r["relations_valid"] = v
        r["relations_requested"] = cur.get("relations_requested", v)
        r["relations_declined"] = 0
        r["relations_errored"] = 0
        r["relation_failures"] = []
        fp = cur.get("ac_fp_count", 0)
        r["ac_verdicts"] = _verdicts(fp, cur.get("ac_relations", v))
        r["ac_fp_count"] = fp
        r["ac_fp_reason"] = None
        wa_labels, wa_verdicts, wa_reasons = [], {}, {}
        for cells in cur["wa_rows"]:
            label = cells[0]
            mfrac = _RE_FRAC.search(cells[1])
            if not mfrac:
                continue
            flagged, total = int(mfrac.group(1)), int(mfrac.group(2))
            wa_labels.append(label)
            wa_verdicts[label] = _verdicts(flagged, total)
            if len(cells) >= 4 and cells[3]:
                wa_reasons[label] = cells[3]
        r["wa_labels"] = wa_labels
        r["wa_verdicts"] = wa_verdicts
        r["wa_reasons"] = wa_reasons

    if "num_goldens" in cur:
        corpus = []
        for cells in cur["golden_rows"]:
            idx = cells[0]
            try:
                idx = int(idx)
            except ValueError:
                pass
            gate = cells[1].strip("`")
            gt_raw = cells[2].strip("`")
            note = cells[5] if len(cells) > 5 else ""
            rec = {"index": idx, "gate": gate}
            if gate == "pass":
                rec["ground_truth"] = _relabel_ground_truth(gt_raw, note)
                ex = _RE_FRAC.search(cells[3])
                sm = _RE_FRAC.search(cells[4])
                rec["meta_example_verdicts"] = (
                    _verdicts(int(ex.group(1)), int(ex.group(2))) if ex else []
                )
                rec["meta_samples_verdicts"] = (
                    _verdicts(int(sm.group(1)), int(sm.group(2))) if sm else []
                )
                if note and rec["ground_truth"] != "correct":
                    rec["gt_witness"] = note
            elif note:
                rec["gate_reason"] = note
            corpus.append(rec)
        r["goldens"] = {
            "num_goldens": cur.get("num_goldens", len(corpus)),
            "gate_passed": cur.get("gate_passed",
                                   sum(1 for g in corpus if g.get("gate") == "pass")),
            "corpus": corpus,
        }
    return r


def relabel_timeouts(results):
    """Apply the wrong->slow relabel in place (idempotent)."""
    for r in results:
        gr = r.get("goldens")
        if not gr:
            continue
        for g in gr.get("corpus", []):
            if g.get("gate") == "pass" and g.get("ground_truth") == "wrong":
                g["ground_truth"] = _relabel_ground_truth("wrong", g.get("gt_witness", ""))
    return results


def render(results, provider, model, rounds, samples):
    from collections import Counter
    by_status = dict(Counter(r.get("status", "?") for r in results))
    agg = {
        "problems_attempted": len(results),
        "by_status": by_status,
        "exp_a": _aggregate_experiment_a(results),
    }
    return _format_markdown(provider, model, rounds, samples, agg, results)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parse", help="markdown report to parse back into results")
    ap.add_argument("--merge", nargs="+", help="result JSON files to concatenate")
    ap.add_argument("--relabel-timeouts", action="store_true",
                    help="relabel timed-out 'wrong' goldens as 'slow'")
    ap.add_argument("--json-out", help="write the (merged/relabeled) results as JSON")
    ap.add_argument("--md-out", help="render a combined markdown report")
    ap.add_argument("--provider", default=None)
    ap.add_argument("--model", default=None)
    ap.add_argument("--rounds", type=int, default=None)
    ap.add_argument("--samples", type=int, default=None)
    args = ap.parse_args()

    header = {"provider": "combined", "model": "combined", "rounds": 0, "samples": 0}
    results = []
    if args.parse:
        header, results = parse_markdown(args.parse)
    if args.merge:
        for path in args.merge:
            with open(path, encoding="utf-8") as f:
                results.extend(json.load(f))

    if args.relabel_timeouts:
        relabel_timeouts(results)

    provider = args.provider or header["provider"]
    model = args.model or header["model"]
    rounds = args.rounds if args.rounds is not None else header["rounds"]
    samples = args.samples if args.samples is not None else header["samples"]

    print(f"{len(results)} problem(s) loaded "
          f"(provider={provider} model={model} R={rounds} S={samples})")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=1)
        print(f"wrote results JSON -> {args.json_out}")
    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(render(results, provider, model, rounds, samples))
        print(f"wrote markdown -> {args.md_out}")
    if not (args.json_out or args.md_out):
        print("(nothing written; pass --json-out and/or --md-out)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
