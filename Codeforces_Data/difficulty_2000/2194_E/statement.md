# E. The Turtle Strikes Back

**Time Limit:** 2 seconds
**Memory Limit:** 512 megabytes

---

## Problem Statement

After a heavy training session, Michelangelo and Raphael decided to order pizza. Today, on the occasion of the holiday, the pizzeria is preparing rectangular pizzas made of $n$ rows and $m$ columns of slices. Each slice has its own unique recipe and flavor.

Michelangelo was the first to open the box and roughly estimated the pleasure of eating each slice: the pleasure from the slice located in the $i$-th row and $j$-th column is equal to $a_{i,j}$. It is guaranteed that there is at least one slice that Michelangelo liked, meaning that among $a_{i, j}$ there is at least one non-negative number.

The turtles agreed that Michelangelo would eat first. According to an ancient tradition, he must choose a route from the top left corner $(1,1)$ to the bottom right corner $(n,m)$ and eat all the slices on that route. In one step, he can move either to the adjacent slice on the right or to the adjacent slice below.

Michelangelo aims to maximize the total pleasure from the eaten slices.

However, Raphael decided to use sauce. Before Michelangelo chooses a route, Raphael decided to choose exactly one slice of pizza and apply his signature sauce to it. But due to the specifics of this sauce, the pleasure from that slice changes to the opposite: if it was previously $a_{i,j}$, after applying the sauce it becomes $-a_{i,j}$.

After that, knowing Raphael's choice, Michelangelo will choose the optimal route for himself and eat all the slices on it.

Raphael became curious about what minimum pleasure Michelangelo could achieve. Help him calculate this number.

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

In the first line of each test case, two integers $n, m\, (1 \le n, m \le 10^6, 1 \leq n \cdot m \le 10^6)$ are given — the number of rows and columns in the table, respectively.

In each of the following $n$ lines of each test case, $m$ integers are provided, separated by spaces. The $j$-th number in the $i$-th of these lines corresponds to the value $a_{i, j}$ ($-10^9 \leq a_{i, j} \leq 10^9$). It is guaranteed that there is at least one non-negative value among the $a_{i, j}$.

It is guaranteed that the sum of $n \cdot m$ across all test cases does not exceed $10^6$

## Output Specification

For each test case, output a single integer — the minimum pleasure Michelangelo can achieve, which Raphael can guarantee.

## Examples

### Example 1

**Input:**
```
2
3 3
1 -2 3
4 -5 2
1 6 -1
2 4
-1 -1 -1 1
-1 -1 -1 -1
```

**Output:**
```
3
-5
```

## Note

If Raphael did not use the sauce, Michelangelo would choose the path $$ (1,1) \rightarrow (2,1) \rightarrow(3,1) \rightarrow (3,2) \rightarrow (3,3) $$ which gives a total pleasure of $1 + 4 + 1 + 6 - 1 = 11$.

However, if Raphael applies the sauce to the cell $(3,2)$, the value $6$ will turn into $-6$. Then the optimal path for Michelangelo will be $$ (1,1) \rightarrow (1,2) \rightarrow (1,3) \rightarrow (2,3) \rightarrow (3,3) $$ with a total pleasure of $1 - 2 + 3 + 2 - 1 = 3$. Raphael cannot achieve a lower result in any cell