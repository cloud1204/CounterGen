import sys
input = sys.stdin.readline

def solve():
    MOD = 998244353
    n, m = map(int, input().split())
    N = n - 1
    max_a_by_b = [0] * (N + 2)
    A_max = 0
    for _ in range(m):
        l, r = map(int, input().split())
        a, b = l, r - 1
        if a > max_a_by_b[b]:
            max_a_by_b[b] = a
        if a > A_max:
            A_max = a
    
    A = [0] * (N + 2)
    cur = 0
    for i in range(1, N + 2):
        if max_a_by_b[i-1] > cur:
            cur = max_a_by_b[i-1]
        A[i] = cur
    
    dp = [0] * (N + 1)
    dp[0] = 1
    S = [0] * (N + 2)
    S[0] = dp[0]
    for i in range(1, N + 1):
        lo = A[i]
        hi = i - 1
        if lo > hi:
            dp[i] = 0
        else:
            if lo == 0:
                dp[i] = S[hi]
            else:
                dp[i] = (S[hi] - S[lo - 1]) % MOD
        S[i] = (S[i-1] + dp[i]) % MOD
    
    ans = 0
    for j in range(A_max, N + 1):
        ans = (ans + dp[j]) % MOD
    ans = ans * 2 % MOD
    print(ans)

t = int(input())
for _ in range(t):
    solve()
