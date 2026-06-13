# C. Twin Polynomials

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

A polynomial $f(x) = a_0 + a_1x + a_2x^2 + \ldots + a_nx^n$ is called a valid polynomial of degree $n$ if and only if $a_i$ is a non-negative integer for all $0 \le i \le n$ and $a_n$ is not $0$.

For a valid polynomial $f(x) = a_0 + a_1x + a_2x^2 + \ldots + a_nx^n$ of degree $n$, its  *twin polynomial*  $g(x)$ is defined as: $$ g(x) = \sum_{i=0}^n i \cdot x^{a_i} $$ For example, for $f(x) = 1 + 2x + 2x^3$, its  *twin polynomial*  is:

$$ g(x) = 0 \cdot x^{1} + 1 \cdot x^{2} + 2 \cdot x^{0} + 3 \cdot x^{2} = 0+x^2+2+3x^2= 2 + 4x^2 $$

A valid polynomial $f(x)$ of degree $n$ is called  *cool*  if and only if $f(x) = g(x)$. In other words, a valid polynomial of degree $n$ is cool if and only if its twin polynomial equals itself.

You are given an incomplete valid polynomial $f(x) = a_0 + a_1x + a_2x^2 + \ldots + a_nx^n$ of degree $n$. Some of $a_i$ have been determined, while others have not been determined. Additionally, it is guaranteed that $a_0$ and $a_n$ are not determined.

Please count the number of  *cool*  valid polynomials of degree $n$ that can be found by determining all undetermined $a_i$'s. Since the answer may be large, you need to output it modulo $1\,000\,000\,007$.

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

For each test case, the first line contains an integer $n$ ($1 \leq n \leq 4 \cdot 10^5$).

The second line contains $n+1$ integers $a_0, a_1, \ldots, a_n$ ($-1 \leq a_i \leq 10^9$). Here, $a_i=-1$ means $a_i$ has not been determined, while $a_i \neq -1$ means $a_i$ has been determined as its value.

It is guaranteed that $a_0$ and $a_n$ are always $-1$ in the input.

It is guaranteed that the sum of $n$ over all test cases does not exceed $4 \cdot 10^5$.

## Output Specification

For each test case, output the number of  *cool*  valid polynomials of degree $n$ found by determining the undetermined $a_i$'s, modulo $1\,000\,000\,007$.

## Examples

### Example 1

**Input:**
```
6
1
-1 -1
2
-1 2 -1
2
-1 -1 -1
3
-1 -1 3 -1
3
-1 2 3 -1
5
-1 -1 -1 1 0 -1
```

**Output:**
```
1
1
3
2
0
3
```

## Note

In the first test case, only $f(x) = x$ satisfies the condition above.

In the second test case, only $f(x) = x^2 + 2x$ satisfies the condition above.

In the third test case, $f(x) = 2x^2 + x$, $f(x) = x^2 + 2x$, and $f(x) = 2x^2 + 1$ satisfy the condition above.