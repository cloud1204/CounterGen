# H. Remove the Grail Tree

**Time Limit:** 3 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

The Great Grail Tree has stood in the kingdom for $315$ years. It takes up a lot of space, so King Ila decided to get rid of it as soon as possible. The tree itself is an acyclic, connected, undirected graph with $n$ vertices, each having its own value $a_v$. The tree can be removed in the following way: 

 - Let $S_v$ be the sum of the values of all remaining neighbors of $v$. If $v$ has no remaining neighbors, then $S_v$ is $0$. Choose a vertex $v$ such that $a_v$ and $S_v$ differ in parity (i.e., either $a_v$ is even and $S_v$ is odd, or $a_v$ is odd and $S_v$ is even). If there are no such vertices, stop the process.
- Remove vertex $v$ and all edges connected to it from the tree.
 Your task is to determine whether there exists a sequence of removals that will lead to the complete removal of the Grail Tree (i.e., no vertices will remain in the tree). If such a sequence exists, output the sequence of $n$ vertices in the order of their removal. If there are multiple answers, output any of them.

## Input Specification

Each test consists of several test case. The first line contains one integer $t$ ($1\le t\le 10^4$) — the number of test cases. The description of the test cases follows.

The first line contains the number $n$ ($1\le n\le 2\cdot 10^5$) — the number of vertices in the Grail Tree.

The second line describes the array $a$ ($1\le a_i\le 10^9$) — the values of the vertices in the tree.

Next, there are $n - 1$ lines, each containing 2 numbers $v$ and $u$ ($1\le v, u\le n, v\neq u$), indicating that vertices $v$ and $u$ are connected by an edge in the tree.

It is guaranteed that the sum of $n$ across all test cases does not exceed $2\cdot 10^5$.

## Output Specification

For each test case, output "YES" if it is possible to completely remove the Grail Tree. Otherwise, output "NO". If the answer is "YES", output any sequence of removals.

You can output each letter in any case (lowercase or uppercase). For example, the strings "yEs", "yes", "Yes", and "YES" will be accepted as a positive answer.

## Examples

### Example 1

**Input:**
```
5
3
1 2 4
1 2
2 3
4
3 4 2 1
1 2
2 3
3 4
6
9 6 5 1 7 4
1 2
2 3
2 4
3 5
4 6
5
2 1 1 1 2
2 1
3 2
2 4
5 4
5
1 5 3 7 9
1 2
2 3
3 4
4 5
```

**Output:**
```
NO
YES
2 3 1 4 
NO
YES
1 5 2 3 4 
YES
2 4 1 5 3
```