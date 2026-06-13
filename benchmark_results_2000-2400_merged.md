# Metamorphic Benchmark Results — Merged (difficulty 2000–2400)

- **Provider:** Mixed — 2000–2100 via **OpenRouter** (`anthropic/claude-opus-4-7`); 2200–2400 via **Claude** direct (`claude-opus-4-7`)
- **Relations per problem (R = rounds):** 3
- **Samples per relation (S):** 10
- **Source runs:** `results_2000-2100_corrected.md` + `benchmark_results.md`
- *Note:* problem `2178_F` was attempted in both runs (metamorphic-error in the 2000–2100 run, TLE in the 2200–2400 run). It is counted **once**, under the 2200 tier from the later run.

## Aggregate

Experiment A measures the metamorphic relation on human submissions, **per generated relation** (each of the R relations is one independent trial).

| Metric | Value |
| --- | --- |
| Problems attempted | 25 |
| Problems that produced relations | 15 |
| Relations generated (valid) | 40 |
| **AC false-positive rate** (per-relation) | **0 / 40 (0.0%)** |
| WA catch rate (per-relation) | 57 / 195 (29.2%) |
| WA catch rate (any relation) | 28 / 71 (39.4%) |
| API calls (both runs, uncached) | 174 |
| API tokens (prompt + completion) | 348404 + 818957 = 1167361 |
| **API cost (both runs)** | **$22.2160** |

### Problem status breakdown

| Status | Count |
| --- | --- |
| `compile-check-failed` | 1 |
| `declined` | 3 |
| `metamorphic-error` | 1 |
| `ok` | 13 |
| `time-limit-exceeded` | 7 |

## Golden-solution evaluation (experiment B)

Does a freshly generated metamorphic relation catch a *wrong LLM golden* that already passed compile + example I/O? Ground truth = differential testing vs the dataset `AC.txt`. A golden is **`wrong-answer`** only if it COMPLETED a run and the checker rejected it; one that times out is shrunk to a smaller input and, if it then agrees, classified **`slow`** (correct-but-too-slow / TLE) rather than wrong. **No AC-based filtering** — the metrics measure how a single generated relation behaves, exactly as the deployed workflow (which has no trusted reference) would use it.

- **Goldens generated:** 95  (**passed existing gate:** 50)
- **Ground truth (gate-pass):** 0 wrong-answer, 38 correct, 12 slow (TLE), 0 unknown
- **Base rate wrong-answer** (of decisive goldens = wrong-answer + correct): **0.0%** — if ~0%, the check is redundant here. `slow` goldens are out of the metamorphic check's scope (the stress tester detects a slow reference itself) and are excluded from the confusion matrix.

### Generated-samples variant (strong)

**Per-relation** (each relation × golden is one trial — the realistic headline):

| | meta FLAGS | meta PASSES |
| --- | --- | --- |
| ground-truth WRONG | 0 (TP) | 0 (FN) |
| ground-truth CORRECT | 0 (FP) | 91 (TN) |

- **Recall on wrong** `TP/(TP+FN)`: **—**
- False-positive rate `FP/(FP+TN)`: 0.0%
- Observations scored: 91

**Any-relation union** (best of the R relations): recall —, FP 0.0%

### Example-only variant (faithful to current AC_generator wiring)

**Per-relation** (each relation × golden is one trial — the realistic headline):

| | meta FLAGS | meta PASSES |
| --- | --- | --- |
| ground-truth WRONG | 0 (TP) | 0 (FN) |
| ground-truth CORRECT | 0 (FP) | 91 (TN) |

- **Recall on wrong** `TP/(TP+FN)`: **—**
- False-positive rate `FP/(FP+TN)`: 0.0%
- Observations scored: 91

**Any-relation union** (best of the R relations): recall —, FP 0.0%

### Per difficulty (generated-samples, per-relation)

| Difficulty | Gate-pass | Base-rate wrong | Recall | FP rate |
| --- | --- | --- | --- | --- |
| 2000 | 20 | 0.0% | — | 0.0% |
| 2100 | 12 | 0.0% | — | 0.0% |
| 2200 | 7 | 0.0% | — | 0.0% |
| 2300 | 7 | 0.0% | — | 0.0% |
| 2400 | 4 | 0.0% | — | — |

## Per difficulty (experiment A)

| Difficulty | Problems | Relations | AC-FP rate | WA catch (per-rel) | WA catch (union) |
| --- | --- | --- | --- | --- | --- |
| 2000 | 5 | 12 | 0.0% | 23.7% | 40.0% |
| 2100 | 5 | 9 | 0.0% | 43.9% | 50.0% |
| 2200 | 5 | 9 | 0.0% | 33.3% | 46.7% |
| 2300 | 5 | 10 | 0.0% | 20.0% | 25.0% |
| 2400 | 5 | 0 | — | — | — |

## Per problem

### `Codeforces_Data\difficulty_2000\2194_E`

**Status:** `ok`  **Time:** 900.1s

**API usage (this run):** 6 calls, 12708+1907=14615 tokens, $0.1112

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 1 / 3 | 33.3% | expected 27 got 3 (k=9) |
| WA3 | 1 / 3 | 33.3% | expected -20 got -5 (k=4) |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 2 | 0.0% |  |

**Goldens:** 5 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `correct` | 0 / 2 | 0 / 2 |  |
| 1 | `pass` | `correct` | 0 / 2 | 0 / 2 |  |
| 2 | `pass` | `correct` | 0 / 2 | 0 / 2 |  |
| 3 | `pass` | `correct` | 0 / 2 | 0 / 2 |  |
| 4 | `pass` | `correct` | 0 / 2 | 0 / 2 |  |

### `Codeforces_Data\difficulty_2000\2195_F`

**Status:** `ok`  **Time:** 421.8s

**API usage (this run):** 8 calls, 17768+5424=23192 tokens, $0.2244

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 3 / 3 | 100.0% | value mismatch for -147665 -289403 671146: 9 vs 8 |
| WA3 | 3 / 3 | 100.0% | value mismatch for 723697 -706566 -415987: 1 vs 0 |
| WA4 | 1 / 3 | 33.3% | mismatch at test case 0 position 0: expected -21346 got 130 |
| WA5 | 3 / 3 | 100.0% | value mismatch for -103 -6 -131: 4 vs 5 |

**Goldens:** 4 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 3 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 4 | `fail` | `—` | — | — | example WA: expected: 3 2 3 3 3 3 2 2 3 3 3 3 1 2  found: |

### `Codeforces_Data\difficulty_2000\2201_C`

**Status:** `ok`  **Time:** 423.4s

**API usage (this run):** 8 calls, 16325+24321=40646 tokens, $0.6897

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 0 / 3 | 0.0% |  |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 3 | 0.0% |  |

**Goldens:** 5 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `slow` | 0 / 3 | 0 / 3 | golden timed out on input: 3381 125994 ((())()()())()(()()())()()(()()())(())()()((()())((()())(((()((()())))()(()())())()()))())((()())(()( |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `pass` | `slow` | 0 / 3 | 0 / 3 | golden timed out on input: 1720 9646 (()((()(()(()((()((((()))))))(((()))(()))()(())(()))(((()((())))())))((((()())))))()()))()(())()()()((( |
| 3 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 4 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |

### `Codeforces_Data\difficulty_2000\2215_B`

**Status:** `ok`  **Time:** 433.3s

**API usage (this run):** 13 calls, 27430+35782=63212 tokens, $1.0317

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 1 / 3 | 33.3% | case 2: original returned -1 but transformed gave a solution |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 1 / 3 | 33.3% | case 19: original solvable but transformed returned -1 |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 3 | 0.0% |  |

**Goldens:** 4 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `fail` | `—` | — | — | example WA: Test case 1: expected a valid permutation but got -1 |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 3 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 4 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |

### `Codeforces_Data\difficulty_2000\2217_E`

**Status:** `declined`  **Time:** 183.8s

**API usage (this run):** 9 calls, 12868+31674=44542 tokens, $0.8562

**Goldens:** 2 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `fail` | `—` | — | — | example WA: expected: 0 0 2 4 5 5 24 9 17 144  found: |
| 1 | `fail` | `—` | — | — | example WA: expected: 0 0 2 4 5 5 24 9 17 144  found: |
| 2 | `pass` | `correct` | — | — |  |
| 3 | `fail` | `—` | — | — | example WA: expected: 0 0 2 4 5 5 24 9 17 144  found: |
| 4 | `pass` | `correct` | — | — |  |

### `Codeforces_Data\difficulty_2100\2150_C`

**Status:** `time-limit-exceeded`  **Time:** 900.1s

**API usage (this run):** 17 calls, 43233+248971=292204 tokens, $6.4404

**Relations:** 1 valid / 3 requested

**AC false-positive:** 0 / 1 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 1 / 1 | 100.0% | expected 6 got 2 |
| WA2 | 0 / 0 | — |  |
| WA3 | 0 / 0 | — |  |
| WA4 | 0 / 0 | — |  |
| WA5 | 0 / 0 | — |  |

**Goldens:** 3 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `slow` | — | — | golden timed out on input: 5059 130480 -16601391 4758248 -4941699 -10424190 5267696 8131440 2761286 -7765714 19817129 -1095578 -16597553 110 |
| 1 | `gen-failed` | `—` | — | — |  |
| 2 | `pass` | `slow` | — | — | golden timed out on input: 2989 86870 129457374 75012344 672 68938976 -126862782 32552101 48853998 43177960 -208467976 244260117 164283537 2 |
| 3 | `fail` | `—` | — | — | example WA: expected: 2 5 0 3000000000 10 85 14 24  found: |
| 4 | `pass` | `slow` | — | — | golden timed out on input: 1614 13498 -353916874 445539606 -101384363 217010056 378152836 510701639 -266208123 -527078757 -81470439 -2159488 |

### `Codeforces_Data\difficulty_2100\2161_D`

**Status:** `time-limit-exceeded`  **Time:** 962.0s

### `Codeforces_Data\difficulty_2100\2170_E`

**Status:** `ok`  **Time:** 770.7s

**API usage (this run):** 12 calls, 19507+30569=50076 tokens, $0.8618

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 3 / 3 | 100.0% | outputs differ: ['733283101', '431060426', '64524591', '197421672', '3584446', '-176397212', '867082360', '15950', '-23313895', '-233506562', '32520', '32', '2', '2', '2', '2', '2', '2', '2', '2', '2' |
| WA2 | 3 / 3 | 100.0% | outputs differ: ['962341951', '558076910', '640138359', '288230919', '31737125', '967995026', '736432489', '152426038', '872921783', '587065896', '200685376', '614216382', '601722871', '64', '2', '32' |
| WA3 | 0 / 3 | 0.0% |  |
| WA4 | 3 / 3 | 100.0% | outputs differ: ['469275832', '4', '516495861', '660040011', '15716493', '837138516', '692221350', '616359454', '607900769', '4032', '4', '4', '6', '4', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2 |
| WA5 | 3 / 3 | 100.0% | outputs differ: ['39400635', '661905890', '507944192', '149906976', '932785144', '805769214', '445589926', '515415726', '602851328', '189958269', '275982564', '49152', '469759880', '192', '248', '6553 |

**Goldens:** 5 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 3 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 4 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |

### `Codeforces_Data\difficulty_2100\2183_E`

**Status:** `ok`  **Time:** 382.9s

**API usage (this run):** 12 calls, 22756+63053=85809 tokens, $1.6901

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 0 / 3 | 0.0% |  |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 3 | 0.0% |  |

**Goldens:** 2 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `fail` | `—` | — | — | exec-timeout on example |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 3 | `fail` | `—` | — | — | example WA: expected: 2 0 10 0 973702700  found: 0 0 10 0 0 |
| 4 | `fail` | `—` | — | — | exec-timeout on example |

### `Codeforces_Data\difficulty_2100\2205_E`

**Status:** `time-limit-exceeded`  **Time:** 900.2s

**API usage (this run):** 12 calls, 22729+153601=176330 tokens, $3.9537

**Relations:** 2 valid / 3 requested

**AC false-positive:** 0 / 2 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 2 / 2 | 100.0% | mismatch: -1640682954 vs 1179675800 |
| WA2 | 0 / 2 | 0.0% |  |
| WA3 | 0 / 2 | 0.0% |  |
| WA4 | 2 / 2 | 100.0% | mismatch: 1079120361246 vs 1044181808891 |
| WA5 | 1 / 2 | 50.0% | mismatch: 1706550252 vs 8686091244 |

**Goldens:** 2 / 5 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `slow` | 0 / 1 | 0 / 1 | golden timed out on input: 7 39 1240 3160 216 2614 831 116 2788 3284 1055 2833 3197 1665 766 2651 1789 269 2308 1607 1454 1922 3005 2 1268 9 |
| 1 | `fail` | `—` | — | — | exec-error on example: Traceback (most recent call last):   File "<string>", line 2, in <module> NameError: name 'n' is not defined |
| 2 | `fail` | `—` | — | — | exec-error on example: Traceback (most recent call last):   File "<string>", line 2, in <module> NameError: name 'np' is not defined |
| 3 | `gen-failed` | `—` | — | — |  |
| 4 | `pass` | `slow` | 0 / 1 | 0 / 1 | golden timed out on input: 9 3663 3182 3018 1636 2337 2800 1321 827 1448 2047 3518 632 391 1866 692 2322 2178 1673 1682 3340 1242 1881 1927 |

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
