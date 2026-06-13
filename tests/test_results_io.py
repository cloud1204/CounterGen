import json
import os
import tempfile
import unittest

from tests import results_io as rio


SAMPLE_MD = """# Metamorphic Benchmark Results

- **Provider:** OpenRouter
- **Model:** `anthropic/claude-opus-4-7`
- **Relations per problem (R = rounds):** 3
- **Samples per relation (S):** 10

## Aggregate

## Per problem

### `Codeforces_Data\\difficulty_2000\\9_X`

**Status:** `ok`  **Time:** 100.0s

**API usage (this run):** 6 calls, 100+20=120 tokens, $0.5000

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 2 / 3 | 66.7% | expected 5 got 4 |
| WA2 | 0 / 3 | 0.0% |  |

**Goldens:** 2 / 3 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `wrong` | 0 / 3 | 0 / 3 | golden timed out on input: 999 |
| 1 | `pass` | `correct` | 0 / 3 | 1 / 3 |  |
| 2 | `fail` | `—` | — | — | example WA: nope |
"""


class ResultsIoTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.md = os.path.join(self.tmp, "r.md")
        with open(self.md, "w", encoding="utf-8") as f:
            f.write(SAMPLE_MD)

    def test_parse_header_and_problem(self):
        header, results = rio.parse_markdown(self.md)
        self.assertEqual(header["model"], "anthropic/claude-opus-4-7")
        self.assertEqual(header["rounds"], 3)
        self.assertEqual(header["samples"], 10)
        self.assertEqual(len(results), 1)
        r = results[0]
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["api_usage"]["cost"], 0.5)
        self.assertEqual(r["relations_valid"], 3)
        # WA verdicts reconstructed: WA1 caught by 2 of 3.
        self.assertEqual(r["wa_verdicts"]["WA1"].count("flag"), 2)
        self.assertEqual(r["wa_verdicts"]["WA2"].count("flag"), 0)
        self.assertIn("expected 5 got 4", r["wa_reasons"]["WA1"])

    def test_relabel_timeouts(self):
        _, results = rio.parse_markdown(self.md)
        # --relabel-timeouts is applied by parse already (via _relabel_ground_truth),
        # but calling it again is idempotent.
        rio.relabel_timeouts(results)
        corpus = results[0]["goldens"]["corpus"]
        g0 = next(g for g in corpus if g["index"] == 0)
        g1 = next(g for g in corpus if g["index"] == 1)
        g2 = next(g for g in corpus if g["index"] == 2)
        self.assertEqual(g0["ground_truth"], "slow")      # was 'wrong' + timed out
        self.assertEqual(g1["ground_truth"], "correct")
        self.assertEqual(g2["gate"], "fail")
        self.assertNotIn("ground_truth", g2)
        # golden 1 (correct) flagged by 1 of 3 relations on the samples variant.
        self.assertEqual(g1["meta_samples_verdicts"].count("flag"), 1)

    def test_mismatch_note_stays_wrong_answer(self):
        self.assertEqual(rio._relabel_ground_truth("wrong", "expected 5 got 4"), "wrong-answer")
        self.assertEqual(rio._relabel_ground_truth("wrong", "golden timed out on input: 9"), "slow")
        self.assertEqual(rio._relabel_ground_truth("wrong", ""), "slow")

    def test_render_and_json_roundtrip(self):
        _, results = rio.parse_markdown(self.md)
        md = rio.render(results, "OpenRouter", "m", 3, 10)
        self.assertIn("Golden-solution evaluation", md)
        self.assertIn("1 slow", md)  # population line: 0 wrong-answer, 1 correct, 1 slow
        path = os.path.join(self.tmp, "out.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f)
        again = json.load(open(path, encoding="utf-8"))
        self.assertEqual(again, results)


if __name__ == "__main__":
    unittest.main()
