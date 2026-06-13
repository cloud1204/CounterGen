# F. Learning Binary Search

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

You step into your first data structures class, where you are learning about binary search. You heard the professor yapping about why binary search works in $O(\log{n})$. But you want to see if you can find a better bound.

Given a sorted array $a$ of size $n$ and an integer $k$, define $f(a, k, l, r)$ as the result of the following code: 

function f(a, k, l, r):   if a does not contain k:      return 0   mid = floor((l+r) / 2)   if a[mid]==k:      return 1   else if a[mid]<k:      return 1+f(a, k, mid+1, r)   else:      return 1+f(a, k, l, mid-1)You are given two integers $n$ and $m$. Define an array $a$ good if:

 - $|a|=n$ (there are $n$ elements in $a$).
- $1 \leq a_1 \leq a_2 \leq \ldots \leq a_n \leq m$ (the array is nondecreasing, bounded by $1$ below and bounded by $m$ above).
 You are interested in finding the sum of $f(a,1,1,n)+f(a,2,1,n)+\ldots+f(a,m,1,n)$ over all good arrays $a$. Since this answer may be huge, output the answer modulo $676\,767\,677$. Note that $676\,767\,677$ is a prime number.

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

The first line of each test case contains two integers $n$ and $m$ ($3 \leq n,m \leq 10^6$).

It is guaranteed that the sum of $n$ does not exceed $10^6$ over all test cases, and the sum of $m$ does not exceed $10^6$ over all test cases.

## Output Specification

For each test case, output the requested sum modulo $676\,767\,677$ on a new line.

## Examples

### Example 1

**Input:**
```
7
3 3
3 4
3 5
4 3
4 5
999967 99967
15 876543
```

**Output:**
```
26
60
115
50
315
93903683
322710644
```

## Note

In the first test case, one good array $a$ is $[2,2,3]$. Here, $f(a,1,1,n)=0$ (as $1$ is not present in $a$), $f(a,2,1,n)=1$, $f(a,3,1,n)=2$. Therefore, the contribution of this good array is $0+1+2=3$.