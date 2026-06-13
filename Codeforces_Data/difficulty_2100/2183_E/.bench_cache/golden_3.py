import sys
from sys import stdin

def solve():
    input_data = stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 998244353
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        m = int(input_data[idx]); idx += 1
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        
        # Check a[0]
        if a[0] != 0 and a[0] != 1:
            results.append(0)
            continue
        
        # Check if n is too large
        if (1 << (n-1)) > m:
            # need a_n >= 2^(n-1), but a_n <= m
            results.append(0)
            continue
        
        # DP: dp[v] = number of ways to reach value v at current position
        dp = [0] * (m + 1)
        # Position 0: must be 1
        if a[0] == 0 or a[0] == 1:
            dp[1] = 1
        else:
            dp[1] = 0
        
        # Precompute divisors of each number up to m
        divisors = [[] for _ in range(m + 1)]
        for d in range(1, m + 1):
            for v in range(d, m + 1, d):
                divisors[v].append(d)
        
        for i in range(1, n):
            new_dp = [0] * (m + 1)
            fixed = a[i] != 0
            for v in range(1, m + 1):
                if dp[v] == 0:
                    continue
                # Next value: v + d where d divides v, d >= 1, v + d <= m
                for d in divisors[v]:
                    nv = v + d
                    if nv > m:
                        break  # divisors are in increasing order? Not guaranteed by construction
                    if fixed and nv != a[i]:
                        continue
                    new_dp[nv] = (new_dp[nv] + dp[v]) % MOD
            dp = new_dp
        
        results.append(sum(dp) % MOD)
    
    print('\n'.join(map(str, results)))

solve()
