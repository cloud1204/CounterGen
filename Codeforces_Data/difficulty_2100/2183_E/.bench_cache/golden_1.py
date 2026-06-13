import sys
input = sys.stdin.readline

def solve():
    MOD = 998244353
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    if a[0] != 0 and a[0] != 1:
        print(0)
        return
    a[0] = 1
    
    # Precompute divisors for each v up to m
    divisors = [[] for _ in range(m+1)]
    for d in range(1, m+1):
        for v in range(d, m+1, d):
            divisors[v].append(d)
    
    # dp[v] = number of sequences of length i ending at v
    dp = [0] * (m+1)
    dp[1] = 1
    
    for i in range(1, n):
        new_dp = [0] * (m+1)
        fixed = a[i]  # 0 means free
        for v in range(1, m+1):
            if dp[v] == 0:
                continue
            for d in divisors[v]:
                w = v + d
                if w > m:
                    break  # divisors are in increasing order
                if fixed != 0 and w != fixed:
                    continue
                new_dp[w] = (new_dp[w] + dp[v]) % MOD
        dp = new_dp
    
    print(sum(dp) % MOD)

t = int(input())
for _ in range(t):
    solve()
