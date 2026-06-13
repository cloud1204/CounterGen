import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    T = list(map(int, input().split()))
    # 1-indexed for clarity, use 0-indexed
    # T[0..n-1]
    # For each start s (0-indexed), compute failure function of T[s..n-1]
    # aperiodic[s][e] = (failure[s][e-s+1] == 0) for substring T[s..e]
    # Actually we don't need to store all, can compute on the fly
    
    # dp[i] for i = 0..n
    dp = [0] * (n + 1)
    dp[0] = 1
    
    # For each start s in 1..n (1-indexed), we want for each end i in s..n,
    # to know if T[s..i] is aperiodic, then add dp[s-1] to dp[i].
    # Using 0-indexed: for each start s0 in 0..n-1, compute failure of T[s0..n-1].
    # The substring T[s0..i0] has length L = i0 - s0 + 1. Aperiodic iff fail[L-1] == 0.
    
    for s in range(n):
        # Compute failure function of T[s..n-1]
        m = n - s
        fail = [0] * m
        # fail[0] = 0
        for k in range(1, m):
            j = fail[k-1]
            while j > 0 and T[s + k] != T[s + j]:
                j = fail[j-1]
            if T[s + k] == T[s + j]:
                j += 1
            fail[k] = j
        # For each end position e = s, s+1, ..., n-1 (0-indexed)
        # Substring T[s..e], length L = e-s+1, aperiodic iff fail[L-1] == 0
        # In dp terms: j (in dp) = s, i = e+1 (dp uses 1-indexed lengths)
        for e in range(s, n):
            L = e - s + 1
            if fail[L-1] == 0:
                dp[e+1] = (dp[e+1] + dp[s]) % MOD
    
    print(dp[n])

t = int(input())
for _ in range(t):
    solve()
