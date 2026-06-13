import sys
input = sys.stdin.readline

def z_function(s):
    n = len(s)
    z = [0]*n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r-i, z[i-l])
        while i+z[i] < n and s[z[i]] == s[i+z[i]]:
            z[i] += 1
        if i+z[i] > r:
            l, r = i, i+z[i]
    return z

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        s = input().strip()
        for _ in range(q):
            l, r = map(int, input().split())
            sub = s[l-1:r]
            z = z_function(sub)
            m = len(sub)
            dp = [0]*(m+1)
            total = 0
            for i in range(1, m+1):
                best = 0
                for j in range(i):
                    if j == 0 or z[j] >= i-j:
                        if dp[j]+1 > best:
                            best = dp[j]+1
                dp[i] = best
                total += best
            print(total)

solve()
