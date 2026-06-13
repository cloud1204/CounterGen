import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = []
    for i in range(n):
        a.append(list(map(int, input().split())))
    
    NEG = float('-inf')
    down = [[NEG]*m for _ in range(n)]
    down[0][0] = a[0][0]
    for i in range(n):
        for j in range(m):
            if i==0 and j==0: continue
            best = NEG
            if i>0: best = max(best, down[i-1][j])
            if j>0: best = max(best, down[i][j-1])
            down[i][j] = best + a[i][j]
    
    up = [[NEG]*m for _ in range(n)]
    up[n-1][m-1] = a[n-1][m-1]
    for i in range(n-1, -1, -1):
        for j in range(m-1, -1, -1):
            if i==n-1 and j==m-1: continue
            best = NEG
            if i<n-1: best = max(best, up[i+1][j])
            if j<m-1: best = max(best, up[i][j+1])
            up[i][j] = best + a[i][j]
    
    diag_max1 = {}
    diag_max2 = {}
    for i in range(n):
        for j in range(m):
            d = i+j
            fv = down[i][j] + up[i][j] - a[i][j]
            if d not in diag_max1:
                diag_max1[d] = fv
                diag_max2[d] = NEG
            else:
                if fv > diag_max1[d]:
                    diag_max2[d] = diag_max1[d]
                    diag_max1[d] = fv
                elif fv > diag_max2[d]:
                    diag_max2[d] = fv
    
    ans = float('inf')
    for i in range(n):
        for j in range(m):
            d = i+j
            fv = down[i][j] + up[i][j] - a[i][j]
            if fv == diag_max1[d]:
                m_avoid = diag_max2[d]
            else:
                m_avoid = diag_max1[d]
            cand = max(m_avoid, fv - 2*a[i][j])
            ans = min(ans, cand)
    print(ans)

t = int(input())
for _ in range(t):
    solve()
