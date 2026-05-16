# E. Definitely Larger

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

You are given a permutation $p$$^{\text{∗}}$ of integers from $1$ to $n$.

For an arbitrary permutation $q$ of length $n$, we say that index $j$  *dominates*  index $i$ if and only if all of the following conditions hold: 

 - $j  \gt  i$,
- $p_j  \gt  p_i$, and
- $q_j  \gt  q_i$.
You are also given an array $d$ of length $n$, where $d_i$ denotes the number of indices that dominate index $i$.

Your task is to construct a permutation $q$ of integers from $1$ to $n$ such that for every index $i$ ($1 \le i \le n$), the number of indices $j$ that dominate $i$ is exactly $d_i$.

If such $q$ exists, output any valid one. Otherwise, report that it does not exist.

---

*$^{\text{∗}}$A permutation of length $n$ is an array consisting of $n$ distinct integers from $1$ to $n$ in arbitrary order. For example, $[2,3,1,5,4]$ is a permutation, but $[1,2,2]$ is not a permutation ($2$ appears twice in the array), and $[1,3,4]$ is also not a permutation ($n=3$ but there is $4$ in the array).*

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 1000$). The description of the test cases follows. 

The first line of each test case contains an integer $n$ ($1 \le n \le 5000$).

The second line of each test case contains $n$ integers $p_1, p_2, \ldots, p_n$. It is guaranteed that $p$ forms a permutation of integers from $1$ to $n$.

The third line of each test case contains $n$ integers $d_1, d_2, \ldots, d_n$ ($0 \le d_i \le n$).

It is guaranteed that the sum of $n$ over all test cases does not exceed $5000$.

## Output Specification

For each test case: 

 - If it is possible to construct $q$, output a line containing $n$ integers $q_1, q_2, \ldots, q_n$ — a valid permutation. If multiple valid answers exist, you may output any of them.
- Otherwise, output $-1$.

## Examples

### Example 1

**Input:**
```
7
3
2 3 1
1 0 0
4
3 4 1 2
2 1 1 0
5
2 3 1 4 5
2 2 1 1 0
1
1
0
5
3 1 4 2 5
1 1 1 1 0
4
3 4 2 1
1 1 1 0
8
7 6 3 1 2 5 4 8
1 1 2 2 2 1 1 0
```

**Output:**
```
1 2 3
-1
2 1 4 3 5
1
2 4 1 3 5
-1
1 2 4 6 5 3 7 8
```

## Note

In the first test case, a valid output is $q = [1, 2, 3]$: 

 - For $i=1$, we have $p_1=2$ and $q_1=1$. The index $j=2$ dominates $i=1$ because $2  \gt  1$, $p_2=3  \gt  p_1$, and $q_2=2  \gt  q_1$. Index $j=3$ does not dominate $i=1$ because $p_3=1  \lt  p_1$. Thus, exactly $1$ index dominates $i=1$, which matches $d_1=1$.
- For $i=2$, we have $p_2=3$ and $q_2=2$. The only larger index is $j=3$, but $p_3=1  \lt  p_2$, so it does not dominate. Thus, $0$ indices dominate $i=2$, matching $d_2=0$.
- For $i=3$, there are no larger indices $j  \gt  3$, so $0$ indices dominate, matching $d_3=0$.
In the second test case, $p = [3, 4, 1, 2]$ and $d = [2, 1, 1, 0]$. Let's look at $i=2$, where $p_2=4$. Since there is no index $j  \gt  2$ with $p_j  \gt  p_2$, no index can dominate $i=2$. However, the array $d$ requires $d_2=1$, which makes it impossible to construct a valid permutation $q$. Hence, the answer is  `-1` .