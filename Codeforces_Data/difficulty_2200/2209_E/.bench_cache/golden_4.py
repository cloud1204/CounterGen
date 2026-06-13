import sys
input = sys.stdin.readline

def z_function(s):
    n = len(s)
    z = [0]*n
    z[0] = n
    l, r = 0, 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r-i, z[i-l])
        while i+z[i] < n and s[z[i]] == s[i+z[i]]:
            z[i] += 1
        if i+z[i] > r:
            l, r = i, i+z[i]
    return z

def solve():
    n, q = map(int, input().split())
    s = input().strip()
    for _ in range(q):
        l, r = map(int, input().split())
        sub = s[l-1:r]
        L = len(sub)
        z = z_function(sub)
        total = 0
        for m in range(1, L+1):
            dp = [0]*(m+1)
            for i in range(1, m+1):
                best = 0
                for p in range(1, i+1):
                    start = i-p
                    if start == 0:
                        match = m
                    else:
                        match = min(z[start], m-start)
                    if match >= p:
                        if dp[start]+1 > best:
                            best = dp[start]+1
                dp[i] = best
            total += dp[m]
        print(total)

t = int(input())
for _ in range(t):
    solve()
