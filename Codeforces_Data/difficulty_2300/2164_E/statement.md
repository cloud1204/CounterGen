# E. Journey

**Time Limit:** 3 seconds
**Memory Limit:** 512 megabytes

---

## Problem Statement

You are on an undirected connected graph of $n$ vertices and $m$ weighted edges. The edges are indexed from $1$ to $m$. The $i$-th edge connects vertex $u_i$ and $v_i$, and has weight $w_i$. You decided to take a wonderful journey around the graph.

Suppose you are at vertex $x$. You can do the following operations any number of times: 

 - *Mark*  an edge connecting $x$ and $y$, take photos along the edge, and move to $y$, which costs exactly the edge's weight.
- *Transfer*  to another arbitrary vertex $z \neq x$ by train. You may choose any path $x\leadsto z$ (not necessarily simple), and the cost is the weight of the edge with the maximum index on that path. Formally, suppose you choose the path with edge indices $e_1, e_2, \ldots, e_k$, such that there exists an array of vertices $p_1, p_2, \ldots, p_{k+1}$ where $x = p_1$, $z = p_{k+1}$, and for all $i$ in $[1, k]$, edge $e_i$ connects $p_{i}$ and $p_{i+1}$, the cost is $w_{\max_{i=1}^k e_i}$.
You are now at vertex $1$, and you need to  *mark*  every edge at least once and return to vertex $1$. Calculate the minimum cost.

Please note the cost for  *transferring*  is not the maximum weight on the path, nor the maximum index itself. If you have any questions, refer to the  *Note*  section below.

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $T$ ($1 \le T \le 10^4$). The description of the test cases follows. 

The first line of each test case contains two integers $n$ and $m$ ($1 \le n \le 10^6$, $0 \le m \le 10^6$).

Then $m$ lines, the $i$-th line contains three integers $u_i, v_i, w_i$ ($1 \le u_i, v_i \le n$, $1 \le w \le 10^9$) — meaning that the edge with index $i$ is between vertex $u_i$ and vertex $v_i$ with weight $w_i$.

It's guaranteed that the described graph is connected.

Also note that the graph may have self-loops and multiple edges.

It is guaranteed that the sums of $n$ and $m$ over all test cases do not exceed $10^6$ each.

## Output Specification

For each test case output one integer — the minimum cost.

## Examples

### Example 1

**Input:**
```
5
5 6
2 4 15
2 5 4
1 3 6
2 3 9
1 2 10
3 4 7
4 3
1 2 3
1 3 2
1 4 1
2 3
1 2 1
2 1 3
1 1 4
6 6
2 3 10
1 3 10
5 6 10
6 6 1
4 5 10
3 4 10
5 5
1 2 4
5 1 5
4 3 6
2 4 10
1 4 7
```

**Output:**
```
58
8
8
71
43
```

## Note

Visualizer link

Let $u \xrightarrow{e} v$ denote going to vertex $v$ from vertex $u$ by edge $e$. 

In the first test case, one possible solution is:

 - Initially, you are at vertex $1$.
- Mark edge $3$ and move to vertex $3$, costs $6$.
- Mark edge $6$ and move to vertex $4$, costs $7$.
- Mark edge $1$ and move to vertex $2$, costs $15$.
- Mark edge $4$ and move to vertex $3$, costs $9$.
- Transfer to vertex $5$. By choosing path $3 \xrightarrow{6} 4 \xrightarrow{1} 2 \xrightarrow{2} 5$, we can achieve cost $7$, since the maximum index among the edges on the path is $6$, and $w_6 = 7$. Note that we don't care about the maximum weight on the path when using operation 2.
- Mark edge $2$ and move to vertex $2$, costs $4$.
- Mark edge $5$ and move to vertex $1$, costs $10$.
The total cost is $6+7+15+9+7+4+10=58$.

In the second test case, one possible solution is:

 - Mark edge $1$ and move to vertex $2$, costs $3$.
- Transfer to vertex $3$ by $2 \xrightarrow{1} 1 \xrightarrow{3} 4 \xrightarrow{3} 1 \xrightarrow{2} 3$, costs $1$. Note the path chosen in operation 2 may not be simple.
- Mark edge $2$ and move to vertex $1$, costs $2$.
- Mark edge $3$ and move to vertex $4$, costs $1$.
- Transfer to vertex $1$ by $4 \xrightarrow{3} 1$, costs $1$.