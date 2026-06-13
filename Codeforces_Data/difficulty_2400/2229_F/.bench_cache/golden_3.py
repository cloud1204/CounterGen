import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    results = []
    for _ in range(t):
        n, k = int(input_data[idx]), int(input_data[idx+1]); idx+=2
        a = [int(input_data[idx+i]) for i in range(n)]; idx+=n
        # dp[mask] = set of sorted tuples
        dp = [set() for _ in range(1<<n)]
        dp[0].add(tuple([0]*k))
        ans = 0
        for mask in range(1<<n):
            if not dp[mask]: continue
            if mask == (1<<n)-1:
                for state in dp[mask]:
                    ans = max(ans, max(state))
                continue
            for i in range(n):
                if mask & (1<<i): continue
                for state in dp[mask]:
                    new_state = list(state)
                    new_state[0] += a[i]
                    new_state.sort()
                    dp[mask|(1<<i)].add(tuple(new_state))
        results.append(ans)
    print('\n'.join(map(str,results)))

solve()
