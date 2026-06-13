import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    MOD = 998244353
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        m = int(input_data[idx]); idx+=1
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        # Precompute divisors of each w
        divisors = [[] for _ in range(m+1)]
        for d in range(1, m+1):
            for w in range(2*d, m+1, d):
                divisors[w].append(d)
        # divisors[w] contains all d with d | w and d < w.
        
        if a[0] != 0 and a[0] != 1:
            results.append(0)
            continue
        
        dp = [0]*(m+1)
        dp[1] = 1
        
        ok = True
        for i in range(1, n):
            new_dp = [0]*(m+1)
            ai = a[i]
            if ai != 0:
                # only w = ai
                w = ai
                if w >= 2 and w <= m:
                    s = 0
                    for d in divisors[w]:
                        s += dp[w-d]
                    new_dp[w] = s % MOD
                # else new_dp[w]=0
            else:
                for w in range(2, m+1):
                    s = 0
                    for d in divisors[w]:
                        s += dp[w-d]
                    new_dp[w] = s % MOD
            dp = new_dp
        
        ans = sum(dp) % MOD
        results.append(ans)
    
    print('\n'.join(map(str, results)))

solve()
