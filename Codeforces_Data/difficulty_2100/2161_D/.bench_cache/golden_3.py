import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    cnt = [0]*(n+2)
    first = [0]*(n+2)
    last = [0]*(n+2)
    for i, v in enumerate(a):
        if cnt[v] == 0:
            first[v] = i
        last[v] = i
        cnt[v] += 1
    NEG = -10**18
    dp = [NEG]*(n+2)
    g = [0]*(n+2)
    for v in range(1, n+1):
        if cnt[v] == 0:
            dp[v] = NEG
        else:
            best = 0
            if v >= 2:
                best = max(best, g[v-2])
            if v >= 1 and cnt[v-1] > 0 and dp[v-1] != NEG:
                if last[v] < first[v-1]:
                    best = max(best, dp[v-1])
            dp[v] = cnt[v] + best
        g[v] = max(g[v-1] if v >= 1 else 0, dp[v])
    print(n - g[n])

t = int(input())
for _ in range(t):
    solve()
