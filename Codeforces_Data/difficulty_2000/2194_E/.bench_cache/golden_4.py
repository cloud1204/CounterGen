import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]
    NEG = float('-inf')
    dp1 = [[NEG]*m for _ in range(n)]
    dp2 = [[NEG]*m for _ in range(n)]
    dp1[0][0] = a[0][0]
    for i in range(n):
        for j in range(m):
            if i==0 and j==0: continue
            best = NEG
            if i>0: best = max(best, dp1[i-1][j])
            if j>0: best = max(best, dp1[i][j-1])
            dp1[i][j] = best + a[i][j]
    dp2[n-1][m-1] = a[n-1][m-1]
    for i in range(n-1,-1,-1):
        for j in range(m-1,-1,-1):
            if i==n-1 and j==m-1: continue
            best = NEG
            if i<n-1: best = max(best, dp2[i+1][j])
            if j<m-1: best = max(best, dp2[i][j+1])
            dp2[i][j] = best + a[i][j]
    
    # For each diagonal d, collect f(r) = dp1[r][d-r]+dp2[r][d-r]-a[r][d-r]
    # find top two with indices
    diag_top = {}  # d -> (max_val, max_r, second_val)
    for d in range(n+m-1):
        rmin = max(0, d-m+1)
        rmax = min(n-1, d)
        best1 = NEG; r1 = -1; best2 = NEG
        for r in range(rmin, rmax+1):
            c = d - r
            f = dp1[r][c] + dp2[r][c] - a[r][c]
            if f > best1:
                best2 = best1
                best1 = f
                r1 = r
            elif f > best2:
                best2 = f
        diag_top[d] = (best1, r1, best2)
    
    ans = float('inf')
    for i in range(n):
        for j in range(m):
            d = i+j
            P = dp1[i][j] + dp2[i][j] - a[i][j]
            best1, r1, best2 = diag_top[d]
            A = best1 if r1 != i else best2
            cand = max(P - 2*a[i][j], A)
            if cand < ans:
                ans = cand
    print(ans)

t = int(input())
for _ in range(t):
    solve()
