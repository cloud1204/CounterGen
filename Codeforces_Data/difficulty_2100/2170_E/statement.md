# E. Binary Strings and Blocks

**Time Limit:** 2 seconds
**Memory Limit:** 512 megabytes

---

## Problem Statement

Define a block in a binary string (a string consisting of characters  `0`  and/or  `1` ) as its continuous substring of characters of the same type that cannot be extended either to the left or to the right. For example, in the string  `110001111` , there are three blocks:

 - `11`  (from the $1$-st character to the $2$-nd character);
- `000`  (from the $3$-rd character to the $5$-th character);
- `1111`  (from the $6$-th character to the $9$-th character).
The substring from the $7$-th character to the $9$-th character  `111`  is not a block because it can be extended to the left. The substring from the $1$-st character to the $5$-th character  `11000`  is not a block because it contains characters of different types.

We call a string  *beautiful*  if we can remove exactly one block from it so that the resulting string consists of an odd number of blocks. For example:

 - the string  `110001111`  is beautiful because we can remove the block from the $3$-rd to the $5$-th character, resulting in the string  `111111` , which consists of one block;
- the string  `1010`  is beautiful because we can remove the block from the $1$-st to the $1$-st character, resulting in the string  `010` , which consists of three blocks;
- the string  `0000`  is not beautiful because the only way to remove a block from it will result in an empty string, which consists of $0$ blocks.
You are given an integer $n$ and $m$ constraints, the $i$-th of which is described by a pair of integers $l_i, r_i$. We denote the substring of the string $s$ from character $l$ to character $r$ inclusive as $s[l:r]$, that is, $s[l:r] = s_l s_{l+1} \dots s_r$. Your task is to count the number of binary strings $s$ of length $n$ meeting the following condition:

 - for each $i$ from $1$ to $m$, the string $s[l_i:r_i]$ is beautiful.

## Input Specification

The first line contains one integer $t$ ($1 \le t \le 10^4$) — the number of test case.

The first line of each test case contains two integers $n$ and $m$ ($2 \le n \le 3 \cdot 10^5$; $1 \le m \le 3 \cdot 10^5$) — the required length of the string and the number of constraints, respectively.

Next, there are $m$ lines, the $i$-th of which contains two integers $l_i, r_i$ ($1 \le l_i  \lt  r_i \le n$) — the description of the $i$-th constraint.

Additional constraints on the input:

 - The sum of $n$ across all test cases does not exceed $3 \cdot 10^5$;
- The sum of $m$ across all test cases does not exceed $3 \cdot 10^5$.

## Output Specification

For each test case, print one integer — the number of strings that satisfy the condition. Since it may be huge, output it modulo $998244353$.

## Examples

### Example 1

**Input:**
```
3
4 3
1 2
2 3
3 4
4 2
1 2
3 4
200 1
13 37
```

**Output:**
```
2
4
570529459
```

## Note

In the first example from the statement, the following strings are suitable:  `1010` ,  `0101` . For each of these strings, both $s[1:2]$, $s[2:3]$, and $s[3:4]$ are beautiful.