# Metamorphic Benchmark Results

- **Provider:** OpenRouter
- **Model:** `anthropic/claude-opus-4-7`
- **Relations per problem (R = rounds):** 3
- **Samples per relation (S):** 5

## Aggregate

Experiment A measures the metamorphic relation on human submissions, **per generated relation** (each of the R relations is one independent trial).

| Metric | Value |
| --- | --- |
| Problems attempted | 1 |
| Problems that produced relations | 1 |
| Relations generated (valid) | 3 |
| **AC false-positive rate** (per-relation) | **0 / 3 (0.0%)** |
| WA catch rate (per-relation) | 0 / 15 (0.0%) |
| WA catch rate (any relation) | 0 / 5 (0.0%) |

### Problem status breakdown

| Status | Count |
| --- | --- |
| `ok` | 1 |

## Golden-solution evaluation (experiment B)

Does a freshly generated metamorphic relation catch a *wrong LLM golden* that already passed compile + example I/O? Ground truth = differential testing vs the dataset `AC.txt` (a `correct` label means *not falsified within the input budget*, not a proof). **No AC-based filtering** — the metrics measure how a single generated relation behaves, exactly as the deployed workflow (which has no trusted reference) would use it.

- **Goldens generated:** 3  (**passed existing gate:** 3)
- **Ground truth (gate-pass):** 2 wrong, 1 correct, 0 unknown
- **Base rate wrong** (of labeled gate-pass goldens): **66.7%** — if ~0%, the check is redundant here

### Generated-samples variant (strong)

**Per-relation** (each relation × golden is one trial — the realistic headline):

| | meta FLAGS | meta PASSES |
| --- | --- | --- |
| ground-truth WRONG | 0 (TP) | 6 (FN) |
| ground-truth CORRECT | 0 (FP) | 3 (TN) |

- **Recall on wrong** `TP/(TP+FN)`: **0.0%**
- False-positive rate `FP/(FP+TN)`: 0.0%
- Observations scored: 9

**Any-relation union** (best of the R relations): recall 0.0%, FP 0.0%

### Example-only variant (faithful to current AC_generator wiring)

**Per-relation** (each relation × golden is one trial — the realistic headline):

| | meta FLAGS | meta PASSES |
| --- | --- | --- |
| ground-truth WRONG | 0 (TP) | 6 (FN) |
| ground-truth CORRECT | 0 (FP) | 3 (TN) |

- **Recall on wrong** `TP/(TP+FN)`: **0.0%**
- False-positive rate `FP/(FP+TN)`: 0.0%
- Observations scored: 9

**Any-relation union** (best of the R relations): recall 0.0%, FP 0.0%

### Per difficulty (generated-samples, per-relation)

| Difficulty | Gate-pass | Base-rate wrong | Recall | FP rate |
| --- | --- | --- | --- | --- |
| 2000 | 3 | 66.7% | 0.0% | 0.0% |

## Per difficulty (experiment A)

| Difficulty | Problems | Relations | AC-FP rate | WA catch (per-rel) | WA catch (union) |
| --- | --- | --- | --- | --- | --- |
| 2000 | 1 | 3 | 0.0% | 0.0% | 0.0% |

## Per problem

### `Codeforces_Data\difficulty_2000\2201_C`

**Status:** `ok`  **Time:** 400.0s

**Relations:** 3 valid / 3 requested

**AC false-positive:** 0 / 3 relations flagged the human AC

| WA | Caught by / relations | Rate | Reason |
| --- | --- | --- | --- |
| WA1 | 0 / 3 | 0.0% |  |
| WA2 | 0 / 3 | 0.0% |  |
| WA3 | 0 / 3 | 0.0% |  |
| WA4 | 0 / 3 | 0.0% |  |
| WA5 | 0 / 3 | 0.0% |  |

**Goldens:** 3 / 3 passed gate

| # | Gate | Ground truth | meta(example) flagged | meta(samples) flagged | Note |
| --- | --- | --- | --- | --- | --- |
| 0 | `pass` | `wrong` | 0 / 3 | 0 / 3 | golden timed out on input: 2838 171940 (()(()()((())())))(())()()((((()()))(()))()(()))()((()()(()))(()(((()((()())()(()))))()(((()())))((() |
| 1 | `pass` | `correct` | 0 / 3 | 0 / 3 |  |
| 2 | `pass` | `wrong` | 0 / 3 | 0 / 3 | golden timed out on input: 1177 40990 ()()((()(((((((((()))))((()())((())))))(()(()))()())(())))(()))(()()((((()())())())))())((((()))()()(( |

