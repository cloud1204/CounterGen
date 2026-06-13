# L. Maximum Color Segment

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

You are given a rope $n$ units long, where each unit is painted either red or black. The rope can be represented as a string of length $n$ consisting of characters  `R`  (red) and  `B`  (black). You are also given two integers $m$ and $k$.

You may perform the following operation at most $m$ times (possibly, zero times):

 - Choose any contiguous substring$^{\text{∗}}$ of the rope of length exactly $k$.
- Flip the color of every unit in the substring: each  `R`  becomes  `B` , and each  `B`  becomes  `R` .
For example, consider the rope  `RRRRBRRR`  with $k = 4$. If you choose the $3$-rd to $6$-th characters ( `RRRRBRRR` ), then after flipping, the rope becomes  `RRBBRBRR` .

Define the number of color segments as the smallest number of contiguous segments into which the rope can be divided so that each segment consists of units of a single color. For instance, the rope  `RRBRRRBB`  has $4$ color segments:  `RR` ,  `B` ,  `RRR` , and  `BB` .

Your task is to determine the maximum possible number of color segments after performing at most $m$ operations.

---

*$^{\text{∗}}$A string $t$ is a substring of a string $s$ if $t$ can be obtained from $s$ by the deletion of several (possibly, zero or all) characters from the beginning and several (possibly, zero or all) characters from the end.*

## Input Specification

The first line contains three integers $n$, $m$, and $k$, representing the length of the rope, the maximum number of operations allowed, and the length of each operation's flip window, respectively.

The second line contains a string of length $n$ consisting only of the characters  `R`  and  `B` , representing the initial content of the rope.

 - $1 \le n \le 3000$
- $0 \le m \le 3000$
- $1 \le k \le n$

## Output Specification

Output an integer in a single line, representing the maximum possible number of color segments after performing at most $m$ operations.

## Examples

### Example 1

**Input:**
```
5 4 3
RRBRR
```

**Output:**
```
5
```

### Example 2

**Input:**
```
10 3 3
RRRRBBRRRB
```

**Output:**
```
8
```

### Example 3

**Input:**
```
7 4 7
RRBRBBR
```

**Output:**
```
5
```