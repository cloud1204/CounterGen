import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n, q = int(input_data[idx]), int(input_data[idx+1]); idx += 2
        s = input_data[idx].decode(); idx += 1
        for _ in range(q):
            l, r = int(input_data[idx]), int(input_data[idx+1]); idx += 2
            T = s[l-1:r]
            m = len(T)
            z = [0]*m
            z[0] = m
            L_, R_ = 0, 0
            for i in range(1, m):
                if i < R_:
                    z[i] = min(R_ - i, z[i - L_])
                while i + z[i] < m and T[z[i]] == T[i + z[i]]:
                    z[i] += 1
                if i + z[i] > R_:
                    L_, R_ = i, i + z[i]
            dp = [0]*(m+1)
            total = 0
            for i in range(1, m+1):
                best = 0
                for L in range(1, i+1):
                    j = i - L
                    if j == 0 or z[j] >= L:
                        if dp[j] + 1 > best:
                            best = dp[j] + 1
                dp[i] = best
                total += best
            out.append(str(total))
    print('\n'.join(out))

solve()
