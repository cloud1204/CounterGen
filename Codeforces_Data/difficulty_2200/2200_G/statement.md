# G. Operation Permutation

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

AksLolCoding has an integer $x$ and a list of $n$ operations. Each operation is a string starting with one of the symbols  `+,-,x,`  or  `/`  (representing addition, subtraction, multiplication, and real number division respectively), followed immediately by a positive integer $y$ ($1 \leq y \leq 10^9$). For example, the operation  `x3`  represents multiplying $x$ by $3$.

AksLolCoding will randomly permute the operations and then apply all operations sequentially to $x$ in the permuted order. Help AksLolCoding compute the expected$^{\text{∗}}$ final value of $x$ modulo $10^9+7$.

Formally, let $M = 10^9 + 7$. It can be shown that the answer can be expressed as an irreducible fraction $\frac{p}{q}$, where $p$ and $q$ are integers and $q \not\equiv 0 \pmod M$. Output the integer equal to $p \cdot q^{-1} \pmod M$. In other words, output such an integer $a$ that $0 \le a  \lt  M$ and $a \cdot q \equiv p \pmod M$.

---

*$^{\text{∗}}$The expected final value of $x$ is the average of the final value of $x$ over all $n!$ permutations.*

## Input Specification

The first line contains a single integer $t$ ($1 \leq t \leq 1000$), the number of test cases.

For each test case, the first line contains two integers $n$ and $x$ ($1 \leq n \leq 3000$, $1 \leq x \leq 10^9$).

The second line of each test case contains $n$ strings, each representing an operation in the format described above.

The sum of $n^2$ over all test cases does not exceed $3000^2$.

Note:  `x`  is used to represent multiplication, not  `*`

## Output Specification

For each test case, output a single integer: the expected final value of $x$ modulo $10^9+7$.

## Examples

### Example 1

**Input:**
```
4
2 10
x2 -10
4 2
+6 +7 /1 -13
8 1
+1 x2 x3 +4 +5 +6 -7 -8
9 864209753
-918273645 x564738291 /365107362 x734582911 -654321789 x998244353 +172519103 /482193765 /482091376
```

**Output:**
```
5
2
166666677
601980218
```

## Note

In the first test case, $x$ can either be $(10\cdot 2)-10=10$ or $(10-10)\cdot 2=0$, resulting in an expected value of $5$.

In the second test case, all possible permutations result in $x=2$.

In the third test case, the expected value of $x$ is $\frac{55}{6}$.