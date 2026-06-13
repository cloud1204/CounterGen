# F. Sum of Fractions

**Time Limit:** 2 seconds
**Memory Limit:** 512 megabytes

---

## Problem Statement

Let's call an  *increase*  of the fraction $\frac{x}{y}$ one of the following operations: 

 - either increase its numerator $x$ by $1$;
- or, if the denominator $y  \gt  1$, decrease its denominator $y$ by $1$.
Note that the fraction is not reduced after the increase. For example, if you have a fraction $\frac{3}{7}$ and you decrease its denominator by $1$, you get $\frac{3}{6}$, not $\frac{1}{2}$.

Suppose you are given an integer array $b_1, b_2, \dots, b_m$ and an integer $k$. You apply the following algorithm: 

 - Construct the array $\frac{1}{b_1}, \frac{1}{b_2}, \dots, \frac{1}{b_m}$.
- Choose any of the fractions and increase it.
- Repeat the previous step $k$ times (the same fraction can be chosen multiple times).
- Calculate the sum of the resulting fractions.
We will denote $\mathrm{MSF}(b, k)$ as the maximum sum of fractions that can be obtained from the array $b$ by applying the increase operation exactly $k$ times.

Let $a[l \dots r]$ be the subarray $a_l, a_{l + 1}, \dots a_r$ of the array $a$.

You are given two arrays of integers $a_1, a_2, \dots, a_n$ and $k_1, k_2, \dots, k_m$. For each $k_i$, calculate $$\left( \sum\limits_{l = 1}^{n}{\sum\limits_{r = l}^{n}\mathrm{MSF}(a[l \dots r], k_i)} \right) \bmod 998\,244\,353.$$ In other words, for each $k_i$, calculate the sum of $\mathrm{MSF}$ over all subarrays of the array $a$ and output the answer modulo.

## Input Specification

The first line contains two integers $n$ and $m$ ($1 \le n, m \le 5 \cdot 10^5$) — the sizes of the arrays $a$ and $k$.

The second line contains $n$ integers $a_1, a_2, \dots, a_n$ ($1 \le a_i \le 10^8$) — the array $a$.

The third line contains $m$ integers $k_1, k_2, \dots, k_m$ ($0 \le k_1 \le k_2 \le \dots \le k_m \le 10^8$) — the array $k$ in non-decreasing order.

## Output Specification

For each $k_i$, output a single integer — the sum of $\mathrm{MSF}$ over all subarrays modulo $998\,244\,353$.

It can be proven that the answer can be represented as an irreducible fraction $\frac{P}{Q}$, where $Q \not\equiv 0 \pmod{998\,244\,353}$. Accordingly, output the answer in the form $P \cdot Q^{-1} \pmod{998\,244\,353}$.

## Examples

### Example 1

**Input:**
```
5 4
2 3 5 2 3
0 1 2 10
```

**Output:**
```
232923695
332748137
931694761
133099397
```

## Note

The answers for the corresponding $k$ are: $\frac{379}{30}$, $\frac{58}{3}$, $\frac{473}{15}$, and $\frac{2249}{15}$.