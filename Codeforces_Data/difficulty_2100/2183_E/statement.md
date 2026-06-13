# E. LCM is Legendary Counting Master

**Time Limit:** 3 seconds
**Memory Limit:** 512 megabytes

---

## Problem Statement

You are given a sequence $a$ of length $n$ and a positive integer $m$. Each element of $a$ is an integer in the range $[0, m]$.

A sequence $a$ is considered good if and only if the following two conditions hold:

 - $a_1 \lt a_2 \lt a_3 \lt \ldots \lt a_n$, and
- $\frac{1}{\operatorname{lcm}(a_1,a_2)}+\frac{1}{\operatorname{lcm}(a_2,a_3)}+\ldots+\frac{1}{\operatorname{lcm}(a_{n-1},a_n)}+\color{red}{\frac{1}{\operatorname{lcm}(a_n,a_1)}}\ge1$.$^{\text{∗}}$
You need to replace all zeros in $a$ with integers from the range $[1, m]$. Calculate the number of different ways to replace the zeros such that the resulting sequence $a$ is good.

Print the answer modulo $998\,244\,353$.

---

*$^{\text{∗}}$The Least common multiple ($\operatorname{lcm}$) of two positive integers is the smallest positive integer that is a multiple of both. For example, $\operatorname{lcm}(2,3)=6, \operatorname{lcm}(4,6)=12$.*

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 1000$). The description of the test cases follows. 

The first line of each test case contains two integers $n$ and $m$ ($2 \le n\le m \le 3000$).

The second line of each test case contains $n$ integers $a_1, a_2, \ldots, a_n$ ($0 \le a_i \le m$).

It is guaranteed that the sum of $m$ over all test cases does not exceed $3000$.

## Output Specification

For each test case, output a single integer — the number of ways to complete the sequence so that it becomes good, modulo $998\,244\,353$.

## Examples

### Example 1

**Input:**
```
5
4 6
1 0 0 6
2 2
2 1
5 24
0 0 4 0 0
5 6
0 0 6 0 0
20 2000
1 0 0 0 0 14 0 0 0 0 0 0 0 0 0 514 0 0 0 0
```

**Output:**
```
2
0
10
0
973702700
```

## Note

In the first test case, there are $2$ ways to replace the zeros such that the sequence becomes good:

 - $[1, 2, 3, 6]$: The sum is $\frac{1}{\operatorname{lcm}(1, 2)} + \frac{1}{\operatorname{lcm}(2, 3)} + \frac{1}{\operatorname{lcm}(3, 6)} + \frac{1}{\operatorname{lcm}(6, 1)} = \frac{1}{2} + \frac{1}{6} + \frac{1}{6} + \frac{1}{6} = 1$.
- $[1, 2, 4, 6]$: The sum is $\frac{1}{\operatorname{lcm}(1, 2)} + \frac{1}{\operatorname{lcm}(2, 4)} + \frac{1}{\operatorname{lcm}(4, 6)} + \frac{1}{\operatorname{lcm}(6, 1)} = \frac{1}{2} + \frac{1}{4} + \frac{1}{12} + \frac{1}{6} = 1$.
In the second test case, the initial sequence is $[2, 1]$. Since $2 \not \lt  1$, the strictly increasing condition is not met, so the answer is $0$.

In the fourth test case, the sequence is fixed to be $[0, 0, 6, 0, 0]$ with $m=6$. The third element is $6$. Since the sequence must be strictly increasing and elements cannot exceed $6$, we would need $6  \lt  a_4  \lt  a_5 \le 6$, which is impossible.