import sys
from sys import stdin

def z_function(s):
    n = len(s)
    z = [0]*n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r-i, z[i-l])
        while i+z[i] < n and s[z[i]] == s[i+z[i]]:
            z[i] += 1
        if i+z[i] > r:
            l, r = i, i+z[i]
    z[0] = n
    return z

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    out = []
    for _ in range(t):
        n, q = int(input_data[idx]), int(input_data[idx+1]); idx+=2
        s = input_data[idx].decode(); idx+=1
        for _ in range(q):
            l, r = int(input_data[idx]), int(input_data[idx+1]); idx+=2
            sub = s[l-1:r]
            m = len(sub)
            z = z_function(sub)
            dp = [-1]*(m+1)
            dp[0] = 0
            for i in range(m):
                if dp[i] < 0: continue
                maxL = m - i if i == 0 else min(z[i], m-i)
                # wait z[0] = m, that's fine
                # from position i, can extend by L in [1, maxL]
                # but maxL means t[i:i+maxL] matches prefix
                # but we need t[i:i+L] == t[0:L] for L<=maxL... yes by z definition
                for L in range(1, maxL+1):
                    if dp[i]+1 > dp[i+L]:
                        dp[i+L] = dp[i]+1
            # sum dp[1..m]
            out.append(str(sum(dp[1:])))
    print('\n'.join(out))

solve()
