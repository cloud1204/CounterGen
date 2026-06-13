import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 998244353
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        m = int(input_data[idx]); idx += 1
        N = n - 1
        INF = N + 2
        minR = [INF] * (N + 2)
        for _ in range(m):
            l = int(input_data[idx]); idx += 1
            r = int(input_data[idx]); idx += 1
            L = l
            R = r - 1
            if R < minR[L]:
                minR[L] = R
        suf = [INF] * (N + 3)
        suf[N + 1] = INF
        for k in range(N, 0, -1):
            suf[k] = min(suf[k + 1], minR[k])
        max_i = [0] * (N + 2)
        for j in range(0, N + 1):
            max_i[j] = suf[j + 1] if j + 1 <= N + 1 else INF
        dp = [0] * (N + 2)
        dp[0] = 1
        prefix = [0] * (N + 3)
        prefix[1] = dp[0]
        jstar = 0
        for i in range(1, N + 1):
            while jstar <= N and max_i[jstar] < i:
                jstar += 1
            if jstar <= i - 1:
                dp[i] = (prefix[i] - prefix[jstar]) % MOD
            else:
                dp[i] = 0
            prefix[i + 1] = (prefix[i] + dp[i]) % MOD
        total = 0
        for j in range(0, N + 1):
            if max_i[j] >= INF:
                total = (total + dp[j]) % MOD
        ans = (2 * total) % MOD
        results.append(ans)
    sys.stdout.write('\n'.join(map(str, results)) + '\n')

solve()
