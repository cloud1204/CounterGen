# C. Rigged Bracket Sequence

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

A regular bracket sequence is a sequence consisting of ' `(` ' and ' `)` ', which can be turned into a valid math expression by inserting $1$ and $+$ any number of times into the sequence. For example, the sequence " `()(()())` " is a regular bracket sequence, while " `())(()` " or " `(()` " are not regular bracket sequences.

You are given a regular bracket sequence $S$.

Let us consider shifting a subsequence$^{\text{∗}}$ to the right. Formally, when a subsequence $S_{i_1} S_{i_2} \ldots S_{i_k}$ is shifted to the right, the characters on the chosen indices simultaneously get reassigned as follows:

 - $S_{i_1} \leftarrow S_{i_k}$;
- $S_{i_2} \leftarrow S_{i_1}$;
- $S_{i_3} \leftarrow S_{i_2}$;
- $\ldots$
- $S_{i_k} \leftarrow S_{i_{k-1}}$.
In other words, the element of the $j$-th chosen index gets reassigned to the $((j-2) \bmod k + 1)$-th chosen character.

For example, when $S$ is " `()(()())` ", shifting the subsequence $S_2 S_4$ changes $S$ to " `((())())` ". On the other hand, shifting $S_2 S_3 S_5$ changes $S$ to " `())((())` ".

Please count how many non-empty subsequences make $S$ remain regular when shifted to the right. As the answer may be huge, you are only asked to output the answer modulo $998\,244\,353$.

---

*$^{\text{∗}}$A sequence $a$ is a subsequence of a sequence $b$ if $a$ can be obtained from $b$ by the deletion of several (possibly, zero or all) element from arbitrary positions. Two subsequences are considered different if the sets of positions of the deleted elements are different.*

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

The first line of each test case contains a single integer $n$ ($2 \le n \le 300\,000$, $n$ is even).

The second line of each test case contains a regular bracket sequence $S$ of length $n$ given as a string without spaces.

It is guaranteed that the sum of $n$ over all test cases does not exceed $300\,000$.

## Output Specification

For each test case, output the answer modulo $998\,244\,353$ on a separate line.

## Examples

### Example 1

**Input:**
```
4
2
()
4
()()
6
(()())
10
()((())())
```

**Output:**
```
2
8
28
312
```

## Note

For the second test case, the $8$ non-empty subsequences that make $S$ remain regular when shifted to the right are as follows:

 - $S_1$: changes $S$ to " `()()` ";
- $S_2$: changes $S$ to " `()()` ";
- $S_3$: changes $S$ to " `()()` ";
- $S_4$: changes $S$ to " `()()` ";
- $S_1 S_3$: changes $S$ to " `()()` ";
- $S_2 S_3$: changes $S$ to " `(())` ";
- $S_2 S_4$: changes $S$ to " `()()` ";
- $S_1 S_2 S_3$: changes $S$ to " `(())` ".