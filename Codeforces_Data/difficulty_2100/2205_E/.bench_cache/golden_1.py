
dp = [0]*(n+1)
dp[0] = 1
MOD = 998244353
for l in range(1, n+1):
    # KMP failure for T[l-1:] (0-indexed)
    s = T[l-1:]  # length n-l+1
    m = len(s)
    fail = [0]*m
    for k in range(1, m):
        j = fail[k-1]
        while j > 0 and s[k] != s[j]:
            j = fail[j-1]
        if s[k] == s[j]:
            j += 1
        fail[k] = j
        if j == 0:
            # T[l..l+k] unbordered; i = l+k
            i = l + k
            dp[i] = (dp[i] + dp[l-1]) % MOD
    # k=0 case: single char unbordered
    dp[l] = (dp[l] + dp[l-1]) % MOD
