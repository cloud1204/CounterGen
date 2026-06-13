import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    NEG = -10**18
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        m = int(input_data[idx]); idx += 1
        a = [0]*(n*m)
        for i in range(n*m):
            a[i] = int(input_data[idx]); idx += 1
        
        f = [NEG]*(n*m)
        f[0] = a[0]
        for i in range(n):
            for j in range(m):
                if i == 0 and j == 0:
                    continue
                k = i*m + j
                best = NEG
                if i > 0:
                    v = f[k-m]
                    if v > best: best = v
                if j > 0:
                    v = f[k-1]
                    if v > best: best = v
                f[k] = best + a[k]
        
        g = [NEG]*(n*m)
        g[n*m-1] = a[n*m-1]
        for i in range(n-1, -1, -1):
            for j in range(m-1, -1, -1):
                if i == n-1 and j == m-1:
                    continue
                k = i*m + j
                best = NEG
                if i < n-1:
                    v = g[k+m]
                    if v > best: best = v
                if j < m-1:
                    v = g[k+1]
                    if v > best: best = v
                g[k] = best + a[k]
        
        through = [0]*(n*m)
        for k in range(n*m):
            through[k] = f[k] + g[k] - a[k]
        
        num_diag = n + m - 1
        diag_max = [NEG]*num_diag
        diag_max_cnt = [0]*num_diag
        diag_second = [NEG]*num_diag
        
        for i in range(n):
            base = i*m
            for j in range(m):
                d = i + j
                v = through[base + j]
                if v > diag_max[d]:
                    diag_second[d] = diag_max[d]
                    diag_max[d] = v
                    diag_max_cnt[d] = 1
                elif v == diag_max[d]:
                    diag_max_cnt[d] += 1
                elif v > diag_second[d]:
                    diag_second[d] = v
        
        ans = None
        for i in range(n):
            base = i*m
            for j in range(m):
                k = base + j
                d = i + j
                v = through[k]
                if v == diag_max[d] and diag_max_cnt[d] == 1:
                    h = diag_second[d]
                else:
                    h = diag_max[d]
                alt = v - 2*a[k]
                cost = h if h > alt else alt
                if ans is None or cost < ans:
                    ans = cost
        
        out.append(str(ans))
    
    sys.stdout.write('\n'.join(out) + '\n')

solve()
