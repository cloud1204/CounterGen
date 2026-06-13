import sys
from sys import stdin

def solve():
    input_data = stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    for _ in range(t):
        n, k = int(input_data[idx]), int(input_data[idx+1]); idx+=2
        a = [int(input_data[idx+i]) for i in range(n)]; idx+=n
        # dp[mask] = set of tuples (sorted bin values)
        dp = [set() for _ in range(1<<n)]
        dp[0].add(tuple([0]*k))
        ans = 0
        for mask in range(1<<n):
            for state in dp[mask]:
                if mask == (1<<n)-1:
                    ans = max(ans, max(state))
                    continue
                mn = state[0]
                for i in range(n):
                    if not (mask>>i)&1:
                        # try adding a[i] to a min bin
                        # all bins with value == mn are candidates
                        # to reduce states, try each unique transition
                        new_states = set()
                        for j in range(k):
                            if state[j] == mn:
                                new_state = list(state)
                                new_state[j] += a[i]
                                new_state.sort()
                                dp[mask | (1<<i)].add(tuple(new_state))
                                break  # all same multiset since min bins are interchangeable
        print(ans)

solve()
