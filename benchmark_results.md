# Metamorphic Benchmark Results

- **Provider:** Claude
- **Model:** `claude-opus-4-7`
- **Relations per problem (R = rounds):** 3
- **Samples per relation (S):** 10

## Aggregate

Experiment A measures the metamorphic relation on human submissions, **per generated relation** (each of the R relations is one independent trial).

| Metric | Value |
| --- | --- |
| Problems attempted | 15 |
| Problems that produced relations | 7 |
| Relations generated (valid) | 19 |
| **AC false-positive rate** (per-relation) | **0 / 19 (0.0%)** |
| WA catch rate (per-relation) | 25 / 95 (26.3%) |
| WA catch rate (any relation) | 12 / 35 (34.3%) |
| API calls (this run, uncached) | 77 |
| API tokens (prompt + completion) | 153080 + 223655 = 376735 |
| **API cost (this run)** | **$6.3568** |

### Problem status breakdown

| Status | Count |
| --- | --- |
| `compile-check-failed` | 1 |
| `declined` | 2 |
| `metamorphic-error` | 1 |
| `ok` | 7 |
| `time-limit-exceeded` | 4 |

## Golden-solution evaluation (experiment B)

Does a freshly generated metamorphic relation catch a *wrong LLM golden* that already passed compile + example I/O? Ground truth = differential testing vs the dataset `AC.txt`. A golden is **`wrong-answer`** only if it COMPLETED a run and the checker rejected it; one that times out is shrunk to a smaller input and, if it then agrees, classified **`slow`** (correct-but-too-slow / TLE) rather than wrong. **No AC-based filtering** — the metrics measure how a single generated relation behaves, exactly as the deployed workflow (which has no trusted reference) would use it.

- **Goldens generated:** 50  (**passed existing gate:** 18)
- **Ground truth (gate-pass):** 0 wrong-answer, 13 correct, 5 slow (TLE), 0 unknown
- **Base rate wrong-answer** (of decisive goldens = wrong-answer + correct): **0.0%** — if ~0%, the check is redundant here. `slow` goldens are out of the metamorphic check's scope (the stress tester detects a slow reference itself) and are excluded from the confusion matrix.

### Generated-samples variant (strong)

**Per-relation** (each relation × golden is one trial — the realistic headline):

| | meta FLAGS | meta PASSES |
| --- | --- | --- |
| ground-truth WRONG | 0 (TP) | 0 (FN) |
| ground-truth CORRECT | 0 (FP) | 27 (TN) |

- **Recall on wrong** `TP/(TP+FN)`: **—**
- False-positive rate `FP/(FP+TN)`: 0.0%
- Observations scored: 27

**Any-relation union** (best of the R relations): recall —, FP 0.0%

### Example-only variant (faithful to current AC_generator wiring)

**Per-relation** (each relation × golden is one trial — the realistic headline):

| | meta FLAGS | meta PASSES |
| --- | --- | --- |
| ground-truth WRONG | 0 (TP) | 0 (FN) |
| ground-truth CORRECT | 0 (FP) | 27 (TN) |

- **Recall on wrong** `TP/(TP+FN)`: **—**
- False-positive rate `FP/(FP+TN)`: 0.0%
- Observations scored: 27

**Any-relation union** (best of the R relations): recall —, FP 0.0%

### Per difficulty (generated-samples, per-relation)

| Difficulty | Gate-pass | Base-rate wrong | Recall | FP rate |
| --- | --- | --- | --- | --- |
| 2200 | 7 | 0.0% | — | 0.0% |
| 2300 | 7 | 0.0% | — | 0.0% |
| 2400 | 4 | 0.0% | — | — |

## Per difficulty (experiment A)

| Difficulty | Problems | Relations | AC-FP rate | WA catch (per-rel) | WA catch (union) |
| --- | --- | --- | --- | --- | --- |
| 2200 | 5 | 9 | 0.0% | 33.3% | 46.7% |
| 2300 | 5 | 10 | 0.0% | 20.0% | 25.0% |
| 2400 | 5 | 0 | — | — | — |

## Per problem

### `Codeforces_Data\difficulty_2200\2178_F`

**Status:** `time-limit-exceeded`  **Time:** 962.2s

**Time limit exceeded** during `hard-cap` (no relation results).

### `Codeforces_Data\difficulty_2200\2200_G`

**Status:** `ok`  **Time:** 364.7s

**API usage (this run):** 6 calls, 10475+950=11425 tokens, $0.0761

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 1 / 3 | 33.3% | Compile Error |
| WA3 | 3 / 3 | 100.0% | outputs differ: ['800893554', '55039742', '415443969', '33541950', '358891236', '631483874', '958598228', '490537771', '109348231', '521973929', '476394776', '978956667', '673983401', '981097761', '34 |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 3 | 0.0% |  |

**Goldens:** 5 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 3 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 4 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |

### `Codeforces_Data\difficulty_2200\2204_F`

**Status:** `ok`  **Time:** 376.1s

**API usage (this run):** 6 calls, 12471+1652=14123 tokens, $0.1037

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 3 / 3 | 100.0% | mismatch: 125241199 vs 427231083 |
| WA4 | 1 / 3 | 33.3% | Compile Error |
| WA5 | 3 / 3 | 100.0% |  |

**Goldens:** 1 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `fail` | `—` | — | — | example WA: expected: 232923695 332748137 931694761 133099397  found: 232923695 382660354 465847396 133099397 |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `fail` | `—` | — | — | example WA: expected: 232923695 332748137 931694761 133099397  found: 232923695 382660354 465847396 133099397 |
| 3 | `fail` | `—` | — | — | example WA: expected: 232923695 332748137 931694761 133099397  found: 232923695 332748137 931694760 110 |
| 4 | `fail` | `—` | — | — | example WA: expected: 232923695 332748137 931694761 133099397  found: 232923695 382660354 465847396 133099397 |

### `Codeforces_Data\difficulty_2200\2207_D`

**Status:** `ok`  **Time:** 684.0s

**API usage (this run):** 10 calls, 19731+34315=54046 tokens, $0.9565

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 3 / 3 | 100.0% | Outputs differ: ['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'yes'] vs ['no |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 0 / 3 | 0.0% |  |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 1 / 3 | 33.3% | candidate crashed on input: |

**Goldens:** 1 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `slow` | 0 / 3 | 2 / 3 |  |
| 1 | `gen-failed` | `—` | — | — |  |
| 2 | `gen-failed` | `—` | — | — |  |
| 3 | `gen-failed` | `—` | — | — |  |
| 4 | `gen-failed` | `—` | — | — |  |

### `Codeforces_Data\difficulty_2200\2209_E`

**Status:** `time-limit-exceeded`  **Time:** 962.0s

**Time limit exceeded** during `hard-cap` (no relation results).

### `Codeforces_Data\difficulty_2300\2159_C`

**Status:** `ok`  **Time:** 461.0s

**API usage (this run):** 8 calls, 14410+25729=40139 tokens, $0.7153

**Relations:** 2 valid / 3 requested (1 declined)

**AC false-positive:** 0 / 2 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 2 / 2 | 100.0% | candidate crashed on input: |
| WA2 | 2 / 2 | 100.0% | candidate crashed on input: |
| WA3 | 2 / 2 | 100.0% | candidate crashed on input: |
| WA4 | 2 / 2 | 100.0% | candidate crashed on input: |
| WA5 | 2 / 2 | 100.0% | candidate crashed on input: |

**Goldens:** 0 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `fail` | `—` | — | — | example WA: expected: 1 1 3 2 0 3  found: |
| 1 | `gen-failed` | `—` | — | — |  |
| 2 | `gen-failed` | `—` | — | — |  |
| 3 | `gen-failed` | `—` | — | — |  |
| 4 | `fail` | `—` | — | — | example WA: expected: 1 1 3 2 0 3  found: 1 1 3 2 0 2 |

### `Codeforces_Data\difficulty_2300\2164_E`

**Status:** `ok`  **Time:** 851.0s

**API usage (this run):** 12 calls, 31175+36404=67579 tokens, $1.0660  ⚠️ **cost cap hit**

**Relations:** 2 valid / 3 requested (1 declined)

**AC false-positive:** 0 / 2 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 2 | 0.0% |  |
| WA2 | 0 / 2 | 0.0% |  |
| WA3 | 0 / 2 | 0.0% |  |
| WA4 | 0 / 2 | 0.0% |  |
| WA5 | 0 / 2 | 0.0% |  |

**Goldens:** 0 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `fail` | `—` | — | — | example WA: expected: 58 8 8 71 43  found: 58 8 8 62 43 |
| 1 | `fail` | `—` | — | — | example WA: expected: 58 8 8 71 43  found: 60 9 8 71 43 |
| 2 | `gen-failed` | `—` | — | — |  |
| 3 | `gen-failed` | `—` | — | — |  |
| 4 | `gen-failed` | `—` | — | — |  |

### `Codeforces_Data\difficulty_2300\2172_L`

**Status:** `ok`  **Time:** 292.2s

**API usage (this run):** 9 calls, 12764+23967=36731 tokens, $0.6630

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 0 / 3 | 0.0% |  |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 3 | 0.0% |  |

**Goldens:** 3 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `gen-failed` | `—` | — | — |  |
| 3 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 4 | `fail` | `—` | — | — | exec-error on example: Traceback (most recent call last):   File "<string>", line 1, in <module> NameError: name 'edges' is not defined |

### `Codeforces_Data\difficulty_2300\2182_F`

**Status:** `ok`  **Time:** 375.6s

**API usage (this run):** 9 calls, 23334+25554=48888 tokens, $0.7555

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 0 / 3 | 0.0% |  |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 3 | 0.0% |  |

**Goldens:** 0 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `fail` | `—` | — | — | example WA: expected: 3 0 4 10 4  found: 0 0 0 0 0 |
| 1 | `fail` | `—` | — | — | example WA: expected: 3 0 4 10 4  found: |
| 2 | `gen-failed` | `—` | — | — |  |
| 3 | `gen-failed` | `—` | — | — |  |
| 4 | `gen-failed` | `—` | — | — |  |

### `Codeforces_Data\difficulty_2300\2187_C`

**Status:** `declined`  **Time:** 291.1s

**API usage (this run):** 8 calls, 17940+25917=43857 tokens, $0.7376

- round 1 (declined): 
- round 2 (declined): 
- round 3 (declined): 

**Goldens:** 4 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `slow` | — | — |  |
| 1 | `pass` | `slow` | — | — |  |
| 2 | `pass` | `slow` | — | — |  |
| 3 | `fail` | `—` | — | — | example WA: expected: 0 2 6 3 23  found: |
| 4 | `pass` | `slow` | — | — |  |

### `Codeforces_Data\difficulty_2400\2193_H`

**Status:** `metamorphic-error`  **Time:** 347.9s

**API usage (this run):** 5 calls, 5520+40960=46480 tokens, $1.0516  ⚠️ **cost cap hit**

- round 1 (metamorphic): per-problem API cost cap reached; skipping further LLM calls
- round 2 (metamorphic): per-problem API cost cap reached; skipping further LLM calls
- round 3 (metamorphic): per-problem API cost cap reached; skipping further LLM calls

**Goldens:** 2 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `correct` | — | — |  |
| 1 | `pass` | `correct` | — | — |  |
| 2 | `gen-failed` | `—` | — | — |  |
| 3 | `fail` | `—` | — | — | exec-error on example: Traceback (most recent call last):   File "<string>", line 188, in <module>   File "<string>", line 35, in solve Unbo |
| 4 | `gen-failed` | `—` | — | — |  |

### `Codeforces_Data\difficulty_2400\2206_F`

**Status:** `compile-check-failed`  **Time:** 28.3s

- WA2 compile error: ValueError: Compile Error

### `Codeforces_Data\difficulty_2400\2207_E`

**Status:** `time-limit-exceeded`  **Time:** 962.0s

**Time limit exceeded** during `hard-cap` (no relation results).

### `Codeforces_Data\difficulty_2400\2211_F`

**Status:** `declined`  **Time:** 183.7s

**API usage (this run):** 4 calls, 5260+8207=13467 tokens, $0.2315

- round 1 (declined): 
- round 2 (declined): 
- round 3 (declined): 

**Goldens:** 2 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `correct` | — | — |  |
| 1 | `gen-failed` | `—` | — | — |  |
| 2 | `fail` | `—` | — | — | exec-timeout on example |
| 3 | `pass` | `correct` | — | — |  |
| 4 | `fail` | `—` | — | — | example WA: expected: 26 60 115 50 315 93903683 322710644  found: |

### `Codeforces_Data\difficulty_2400\2229_F`

**Status:** `time-limit-exceeded`  **Time:** 962.0s

**Time limit exceeded** during `hard-cap` (no relation results).

