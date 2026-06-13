# E. A Trivial String Problem

**Time Limit:** 4 seconds
**Memory Limit:** 1024 megabytes

---

## Problem Statement

Define $f(t)$ as the maximum number of parts $t$ can be split into such that each part is a non-empty prefix of $t$. In other words, $f(t)$ is the maximum positive integer $k$ that satisfies the following condition:

 - There exist $k$ strings $p_1,p_2,\ldots,p_k$, which are prefixes of $t$, such that $t=p_1+p_2+\ldots+p_k$. Here $+$ denotes the string concatenation.
You are given a string $s$ of length $n$, consisting of only lowercase English letters. Let $s[x..y]$ represent the substring$^{\text{∗}}$ of $s$ from the $x$-th to the $y$-th character (inclusive). You need to answer $q$ queries. The $i$-th query provides two integers $l_i$ and $r_i$, and you need to find

$$ \sum_{j=l_i}^{r_i} f(s[l_i..j]). $$

---

*$^{\text{∗}}$A string $a$ is a substring of a string $b$ if $a$ can be obtained from $b$ by the deletion of several (possibly, zero or all) characters from the beginning and several (possibly, zero or all) characters from the end.*

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^3$). The description of the test cases follows. 

The first line of each test case contains two integers $n$ and $q$ ($1 \le n \le 10^6$, $1 \le q \le 100$).

The second line contains the string $s$ of length $n$, consisting of only lowercase English letters.

The $i$-th of the next $q$ lines contains two integers $l_i$ and $r_i$ ($1 \le l_i \le r_i \le n$), representing the $i$-th query.

It is guaranteed that the sum of $n$ over all test cases does not exceed $10^6$.

## Output Specification

For each query, output an integer representing the value of the expression.

## Examples

### Example 1

**Input:**
```
6
1 1
a
1 1
5 2
aaaaa
1 5
2 4
6 2
abcdef
1 6
3 5
6 3
abaaba
1 6
1 3
2 6
7 3
abcabca
1 7
2 7
4 7
8 3
aababaac
1 8
2 8
3 7
```

**Output:**
```
1
15
6
6
3
14
4
7
12
9
5
13
14
7
```

## Note

In the first test case, $f(\texttt{a})=1$.

In the second test case, $f(\texttt{a})+f(\texttt{aa})+f(\texttt{aaa})+f(\texttt{aaaa})+f(\texttt{aaaaa})=1+2+3+4+5=15$ and $f(\texttt{a})+f(\texttt{aa})+f(\texttt{aaa})=1+2+3=6$.

In the third test case, $f(\texttt{a})+f(\texttt{ab})+f(\texttt{abc})+f(\texttt{abcd})+f(\texttt{abcde})+f(\texttt{abcdef})=1+1+1+1+1+1=6$ and $f(\texttt{c})+f(\texttt{cd})+f(\texttt{cde})=1+1+1=3$.