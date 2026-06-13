# C. Jerry and Tom

**Time Limit:** 3 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

Jerry and Tom are playing a game on a directed graph $G$ with $n$ vertices, numbered from $1$ to $n$. For every vertex $1 \le u  \lt  n$, there is a directed edge from $u$ to $u+1$. In addition, there are $m$ extra directed edges. The $i$-th extra edge goes from $u_i$ to $v_i$, where $1 \le u_i  \lt  v_i \le n$.

The graph $G$ has the following special property: there do not exist two directed edges $(u_i\to v_i)$ and $(u_j\to v_j)$ such that $u_i  \lt  u_j  \lt  v_i  \lt  v_j$.

At the beginning of the game, Jerry and Tom stand on vertices $x$ and $y$, respectively, where $x \ne y$. The game proceeds in turns. In each turn, the players behave according to the following rules, with Jerry going first, followed by Tom: 

 - Jerry must choose one outgoing edge from his current vertex and move along it to its end. If his current vertex has no outgoing edges, he stays where he is.
- Tom may choose one outgoing edge from his current vertex and move along it to its end, or choose not to move and stay where he is.
If at the end of any turn, Jerry and Tom are at the same vertex (including at vertex $n$), the game ends immediately and Tom wins. Otherwise, if Jerry is initially at vertex $n$, or reaches vertex $n$ at the end of any turn, Jerry wins.

Note that if after a turn, both Jerry and Tom are at vertex $n$, then Tom wins.

Throughout the entire game, both players know each others' locations.

It can be proven that the game will end in a finite number of turns.

For a pair of integers $1 \le x,y \le n$, $x \ne y$, define $f(x,y)$ as follows:

- Jerry and Tom will play a game, where Jerry starts at vertex $x$ and Tom starts at vertex $y$. Tom wants to win, but he also wants to minimise the number of times he actually moves (that is, the number of turns in which he changes his vertex; staying still does not count as a move). Assuming both players play optimally, let $f(x,y)=0$ if Tom cannot win; otherwise, let $f(x,y)$ be the minimum number of moves Tom has to make in order to force a win. If Tom wins under optimal play, Jerry will still try to maximize the number of moves Tom has to make.
Compute $$\sum\limits_{1 \le x,y \le n, x \ne y}f(x,y).$$

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

The first line of each test case contains two integers $n$ and $m$ ($2 \le n \le 2 \cdot 10^5$, $0 \le m \le n-2$), representing the number of vertices and the number of extra edges, respectively.

The $i$-th of the next $m$ lines contains two integers $u_i$ and $v_i$ ($1 \le u_i,v_i \le n$, $u_i + 1  \lt  v_i$), representing an extra edge. It is guaranteed that for any ordered pair of vertices $(u,v)$, there exists at most one edge from $u$ to $v$. It is guaranteed that there do not exist two directed edges $(u_i\to v_i)$ and $(u_j\to v_j)$ such that $u_i  \lt  u_j  \lt  v_i  \lt  v_j$.

It is guaranteed that the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$.

## Output Specification

For each test case, output an integer representing the value of the expression.

## Examples

### Example 1

**Input:**
```
5
2 0
3 1
1 3
4 2
2 4
1 4
5 1
1 4
8 3
1 4
5 8
2 4
```

**Output:**
```
0
2
6
3
23
```

## Note

In the first test case:

 - $x=1$, $y=2$: Jerry is forced to move to $2$ on the first turn. Then, Tom can wait at $2$. At the end of the first turn, both Jerry and Tom are at $2$, and thus, $f(1,2)=0$ as Tom can win without ever moving.
- $x=2$, $y=1$: Jerry is at $n=2$ at the beginning; Tom cannot force a win. Thus, $f(2,1)=0$.
In the third test case, the pairs of $(x,y)$ such that Tom wins are as follows:

 - For $x=1,2,3$ and $y=4$. No matter where Jerry moves to, Tom can stay at $4$ until Jerry reaches $4$. Tom can win without ever moving. $f(1,4)=f(2,4)=f(3,4)=0$.
- For $x=1,2$ and $y=3$, no matter where Jerry moves to on the first turn, Tom has to move to $4$ on the first turn to guarantee a win. For example, if Jerry starts at $1$ and moves to $4$ through the edge $(1 \to 4)$, but Tom chooses to stay at $3$ on the first turn, Jerry reaches $4$ at the end of the first turn, winning the game. Thus, $f(1,3)=f(2,3)=1$.
- For $x=1,3$ and $y=2$, Tom also has to move to $4$ on the first turn to guarantee a win; $f(1,2)=f(3,2)=1$.
- For $x=2,3$ and $y=1$, Tom still has to move to $4$ on the first turn to guarantee a win; $f(2,1)=f(3,1)=1$.