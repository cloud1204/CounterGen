# F. Load Unbalancing

**Time Limit:** 1.5 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement


You are given a sequence $a$ of length $n$, as well as an integer $k$.

You may first reorder the elements of $a$ however you like. Then, define $f(a)$ as follows: 

 - Let $b$ be an array of length $k$ which is initially all zeros.
- For each $1 \le i \le n$ in order, add $a_i$ to any minimum element of $b$.
- At the end of this process, $f(a) = \max(b)$.
Find the maximum possible value of $f(a)$ among all rearrangements of $a$.

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

The first line of each test case contains two integers $n$ and $k$ ($1 \le k \le n \le 18$).

The second line of each test case contains $n$ integers $a_1, a_2, \ldots, a_n$ ($1 \le a_i \le 10^9$).

It is guaranteed that the sum of $2^n$ over all test cases does not exceed $2^{18}$.

## Output Specification

For each test case, output a single integer — the maximum possible value of $f(a)$ among all rearrangements of $a$.

## Examples

### Example 1

**Input:**
```
1
18 5
837492015 264819073 519603847 902746518 173058264 648291507 395174620 781532946 506847193 924613708 158397042 673029415 240785631 819456270 461302987 730619824 528947163 894271056
```

**Output:**
```
2823249283
```

### Example 2

**Input:**
```
6
4 2
1 2 4 5
1 1
10
8 3
3 4 1 3 2 4 5 3
3 1
1000000000 1000000000 1000000000
17 6
6 7 67 4 1 41 6 9 69 3 1 4 1 5 9 2 6
2 2
1 2
```

**Output:**
```
8
10
11
3000000000
85
2
```

## Note

In the first test case of the second example, one optimal rearrangement of $a$ is $[1, 4, 2, 5]$. $f(a)$ is computed as follows: 

 $i$$a_i$$b$$-$$-$$[0, 0]$$1$$1$$[1, 0]$$2$$4$$[1, 4]$$3$$2$$[3, 4]$$4$$5$$[8, 4]$ After this, $f(a) = \max([8,4]) = 8$. It can be shown that the maximum achievable $f(a)$ is $8$.

In the third test case of the second example, one optimal rearrangement of $a$ is $[3, 1, 2, 3, 5, 4, 3, 4]$.