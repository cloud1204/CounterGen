# E. Simons and Dividing the Rhythm

**Time Limit:** 2 seconds
**Memory Limit:** 512 megabytes

---

## Problem Statement

*I grip my troubles within my hand, then hurl them off a thousand lands.* — SHUN,  *ONMYWAY* Consider that Simons is given an array $a$ of size $m$.

Simons must operate on the array exactly once as follows:

 - First, he has to select an integer $k$ and choose $k$ pairs of integers $[l_1,r_1],[l_2,r_2],\ldots,[l_k,r_k]$, such that: 
 - $l_i\le r_i$ for each $1\le i\le k$,
- $l_1=1$, $r_k=m$, and
- $r_i+1=l_{i+1}$ for each $i$ from $1$ to $k-1$.
- Then, he reverses each subarray $[a_{l_i},a_{l_i+1},\ldots, a_{r_i}]$ independently. After this, the array will become $[a_{r_1},a_{r_1-1},\ldots,a_{l_1},a_{r_2},\ldots,a_{l_{k-1}},a_{r_{k}},a_{r_k-1},\ldots,a_{l_k}]$.
You are given an array $T$ of size $n$. Count the number of arrays $S$ such that Simons can transform $S$ to $T$, modulo $998\,244\,353$.

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 8000$). The description of the test cases follows. 

The first line contains an integer $n$ ($1\le n\le 8000$) — the length of $T$.

The second line contains $n$ integers $T_1,T_2,\ldots,T_n$ ($1\le T_i\le 8000$) — the elements of $T$.

It is guaranteed that the sum of $n$ over all test cases does not exceed $8000$.

## Output Specification

For each test case, output a single integer — the number of arrays $S$, modulo $998\,244\,353$.

## Examples

### Example 1

**Input:**
```
5
4
1 1 2 1
4
1 2 3 1
6
1 3 2 3 3 2
10
2 3 1 4 3 1 4 3 1 2
1
8000
```

**Output:**
```
4
7
22
383
1
```

## Note

In the first test case, we can see only the following arrays can be transformed to $T$:

 - For $S=[2,1,1,1]$, Simons will choose $[1,3]$ and $[4,4]$. Thus, the array will become $[1,1,2,1]$, equal to $T$.
- For $S=[1,2,1,1]$, Simons will choose $[1,4]$.
- For $S=[1,1,2,1]$, Simons will choose $[1,2]$, $[3,3]$, and $[4,4]$.
- For $S=[1,1,1,2]$, Simons will choose $[1,2]$ and $[3,4]$.
In the second test case, we can see only the following arrays can be transformed to $T$:

 - For $S=[1,1,3,2]$, Simons will choose $[1,1]$ and $[2,4]$.
- For $S=[1,2,1,3]$, Simons will choose $[1,1]$, $[2,2]$, and $[3,4]$.
- For $S=[1,2,3,1]$, Simons will choose $[1,1]$, $[2,2]$, $[3,3]$, and $[4,4]$.
- For $S=[1,3,2,1]$, Simons will choose $[1,4]$.
- For $S=[2,1,1,3]$, Simons will choose $[1,2]$ and $[3,4]$.
- For $S=[2,1,3,1]$, Simons will choose $[1,2]$, $[3,3]$, and $[4,4]$.
- For $S=[3,2,1,1]$, Simons will choose $[1,3]$ and $[4,4]$.