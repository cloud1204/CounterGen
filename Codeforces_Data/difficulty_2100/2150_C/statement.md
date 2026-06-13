# C. Limited Edition Shop

**Time Limit:** 2 seconds
**Memory Limit:** 256 megabytes

---

## Problem Statement

*cYsmix - House With Legs* ⠀There is a shop with $n$ objects numbered from $1$ to $n$, and only one copy of each object. According to you, the objects have values $v_1, v_2, \ldots, v_n$ (which can be negative).

Alice and Bob have their own order of preference of objects ($a_1, a_2, \ldots, a_n$ and $b_1, b_2, \ldots, b_n$ respectively). In particular, Alice's favourite object is $a_1$, followed by $a_2$, etc.; Bob's favourite object is $b_1$, followed by $b_2$, etc.

For $n$ times, one of them goes to the shop and buys her or his most favourite object still in the shop. At the end, Alice and Bob have their own sets of objects.

Now the shop is empty, and you wonder whether Alice's preferences are similar to yours. Over all sets of objects that Alice could have bought, what's the maximum sum of values according to you?

## Input Specification

Each test contains multiple test cases. The first line contains the number of test cases $t$ ($1 \le t \le 10^4$). The description of the test cases follows. 

The first line of each test case contains a single integer $n$ ($1 \le n \le 2 \cdot 10^5$) — the number of objects.

The second line of each test case contains $n$ integers $v_1, v_2, \ldots, v_n$ ($-10^9 \le v_i \le 10^9$) — the values of the objects, according to you.

The third line of each test case contains $n$ integers $a_1, a_2, \ldots, a_n$ ($1 \le a_i \le n$) — Alice's order of preference. The $a_i$ are distinct.

The fourth line of each test case contains $n$ integers $b_1, b_2, \ldots, b_n$ ($1 \le b_i \le n$) — Bob's order of preference. The $b_i$ are distinct.

It is guaranteed that the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$.

## Output Specification

For each test case, output a single integer: the maximum sum of values over all sets of objects that Alice could have bought.

## Examples

### Example 1

**Input:**
```
8
3
1 -1 1
3 1 2
2 3 1
3
-2 5 2
3 1 2
2 3 1
3
-1 -2 -3
3 1 2
2 3 1
3
1000000000 1000000000 1000000000
3 1 2
2 3 1
4
5 -15 10 -5
2 4 3 1
1 4 2 3
4
-5 -5 -5 100
2 3 1 4
4 1 2 3
4
-1 -100 5 10
1 2 3 4
2 3 4 1
12
-4 6 10 10 1 -8 6 2 -8 -4 0 -6
11 12 7 3 6 8 1 5 10 2 9 4
7 5 3 6 1 2 8 12 9 4 10 11
```

**Output:**
```
2
5
0
3000000000
10
85
14
24
```

## Note

In the first test case, Alice can buy the sets of objects $[]$ (empty), $[1]$, $[3]$, $[3, 1]$, $[3, 1, 2]$ (the objects are ordered by purchase time). For example, for Alice to buy $[1]$, the two can enter the store in the following order:

 - Bob enters and buys object $2$;
- Bob enters and buys object $3$ (object $2$ is sold out);
- Alice enters and buys object $1$ (object $3$ is sold out).
The set of objects with maximum total value according to you is $[3, 1]$, which has value $v_3 + v_1 = 2$.

In the second test case, Alice's and Bob's preferences are the same as in the first test case, but now the set of objects with maximum total value is $[3, 1, 2]$, with value $5$.