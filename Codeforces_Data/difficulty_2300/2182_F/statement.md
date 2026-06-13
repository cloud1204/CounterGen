# F1. Christmas Reindeer (easy version)

**Time Limit:** 4 seconds
**Memory Limit:** 512 megabytes

---

## Problem Statement

This is the easy version of the problem. The only difference between the versions is the upper bound on $n$ and $m$. In this version, $n \le 500$ and $m \le 500$.

You have a herd of $n$ Christmas reindeer. The strength of the $i$-th reindeer is $2^{c_i}$.

The carrying capacity of a group of $k$ Christmas reindeer is calculated as follows:

 - the strengths of the reindeer are sorted in non-increasing order. Let's denote the sorted list of strengths as $c'_1, c'_2, \dots, c'_k$, where $c'_i \ge c'_{i+1}$;
- then, the carrying capacity of this group of reindeer is equal to $c'_1 + \lfloor\frac{c'_2}{2}\rfloor + \lfloor\frac{c'_3}{4}\rfloor + \dots + \lfloor\frac{c'_k}{2^{k - 1}}\rfloor$.
Note that some reindeer may contribute zero to the carrying capacity of the group.

You have to process queries of three types: 

 - add a reindeer with strength equal to $2^x$ to the herd;
- remove a reindeer with strength equal to $2^x$ from the herd of reindeer;
- calculate the number of ways to choose some of the reindeer from the herd (possibly all of them) so that the carrying capacity of the chosen group is at least $x$.
If there are multiple reindeer with the same strength in the herd, they are considered different. For example, if you have two reindeer with strength $1$ each, and you need to calculate the number of ways to choose a group with carrying capacity of at least $1$, there are $3$ ways to choose it: choose the first reindeer, the second reindeer, or both of them.

## Input Specification

The first line contains two integers $n$ and $m$ ($1 \le n, m \le 500$) — the initial number of reindeer in the herd and the number of queries, respectively.

The second line contains $n$ integers $c_1, c_2, \dots, c_n$ ($0 \le c_i \le 60$) denoting the strengths of the reindeer in the herd: the strength of the $i$-th reindeer is $2^{c_i}$.

The next $m$ lines describe the queries in one of the following formats: 

 - $1$ $x$ ($0 \le x \le 60$) — add a reindeer with strength equal to $2^x$ to the herd;
- $2$ $x$ ($0 \le x \le 60$) — remove a reindeer with strength equal to $2^x$ from the herd;
- $3$ $x$ ($1 \le x \le 10^{18}$) — calculate the number of ways to choose a group of reindeer from the herd so that the carrying capacity of the chosen group is at least $x$.
Additional constraint on the input: whenever a query of type $2$ is given, the herd currently contains at least one reindeer with strength equal to $2^x$.

## Output Specification

For each query of the third type, print a single integer — the number of ways to choose a group of reindeer from the herd (possibly the whole herd) so that the carrying capacity of the chosen group is at least $x$. Since it can be huge, print it modulo $998244353$.

## Examples

### Example 1

**Input:**
```
3 7
2 1 1
3 5
3 6
1 2
3 6
3 5
2 1
3 5
```

**Output:**
```
3
0
4
10
4
```

### Example 2

**Input:**
```
5 5
6 9 2 3 5
3 518
1 4
2 9
1 10
3 1016
```

**Output:**
```
12
32
```

### Example 3

**Input:**
```
5 20
56 58 31 56 57
3 584133699915613698
1 26
3 718934517698133644
1 43
3 853795525565803934
3 371128907885602007
1 54
1 25
3 12283451778216771
2 25
3 269837405423769340
1 0
3 81332884431075468
1 23
3 4256984962444022
3 668408003982766102
3 923410222653374550
3 340313743235311415
3 550166282440775769
3 445344499963496530
```

**Output:**
```
0
0
0
24
496
128
416
992
0
0
320
0
0
```

## Note

Let's consider the first example. Initially, there are three reindeer with strength equal to $4$, $2$ and $2$, respectively.

 - during the first query, you have to calculate the number of ways to choose a group with carrying capacity of at least $5$. There are three possible groups: $\{1, 2\}$ (the group containing the $1$-st and the $2$-nd reindeer), $\{1, 2, 3\}$, and $\{1, 3\}$;
- during the second query, you have to calculate the number of ways to choose a group with carrying capacity of at least $6$. Even the whole herd has carrying capacity equal to $4 + \lfloor\frac{2}{2}\rfloor + \lfloor\frac{2}{4}\rfloor = 5$, so there are no suitable ways to choose a group;
- during the third query, a reindeer with strength $4$ is added. Let's denote it as the $4$-th reindeer;
- during the fourth query, the possible groups are $\{1, 4\}$, $\{1, 2, 4\}$, $\{1, 3, 4\}$ and $\{1, 2, 3, 4\}$;
- during the fifth query, there are $10$ possible groups;
- during the sixth query, a reindeer with strength $2$ is removed. Let's say that it was the $2$-nd reindeer, so only reindeer $1, 3, 4$ remain;
- during the seventh query, you have to calculate the number of ways to choose a group with carrying capacity of at least $5$. There are four possible groups: $\{1, 3\}$, $\{1, 4\}$, $\{1, 3, 4\}$, $\{3, 4\}$.