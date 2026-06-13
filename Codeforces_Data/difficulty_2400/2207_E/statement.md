# E2. N-MEX (Counting Version)

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

The Master Builder doesn't like repetitive tasks — repairing the base, upgrading the town hall fifteen times, and doing yet more programming problems about MEX. So, this is not going to be your ordinary MEX problem.

For any positive integer $k$, define the  *$k$-mex*  of a collection of integers $S$ to be the $k$-th smallest nonnegative integer not present in $S$. For instance, the $1$-mex and $2$-mex of $[1, 2, 1]$ are $0$ and $3$, respectively.

Let $n$ be a positive integer, and consider an array of nonnegative integers $[a_1, \ldots, a_n]$. Compute the number of arrays of nonnegative integers $[b_1, \ldots, b_n]$ such that: 

 - For all $1 \leq i \leq n$, the $(n-i+1)$-mex of $[b_1, \ldots, b_i]$ is $a_i$.
- Additionally, for all $1 \leq i \leq n$, $0 \leq b_i \leq n$.
 Since the number of such arrays may be large, output the answer modulo $10^9 + 7$.

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

The first line of each test case contains a single integer $n$ ($1 \leq n \leq 2 \cdot 10^5$) — the length of the array $a$.

The second line of each test case contains $n$ integers $a_1, \ldots, a_n$ ($0 \leq a_i \leq 10^9$).

It is guaranteed that the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$.

## Output Specification

For each test case, output a single integer — the number of satisfying arrays $b$ modulo $10^9 + 7$.

## Examples

### Example 1

**Input:**
```
6
3
3 3 1
3
2 1 3
1
0
1
2
4
7 5 2 2
6
6 6 6 4 3 3
```

**Output:**
```
6
0
1
0
0
360
```

## Note

In the first test case, the array $a = [3, 3, 1]$. There exist exactly six such arrays $b$ that work. One such example is the array $b = [2, 0, 2]$, which satisfies the conditions because: 

 - the $3$-mex of $[b_1] = [2]$ is $a_1 = 3$,
- the $2$-mex of $[b_1, b_2] = [2, 0]$ is $a_2 = 3$,
- the $1$-mex of $[b_1, b_2, b_3] = [2, 0, 2]$ is $a_3 = 1$.
In the second test case, the array $a = [2, 1, 3]$. It can be shown that no suitable array $b$ exists.