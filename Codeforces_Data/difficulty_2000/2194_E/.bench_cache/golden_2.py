import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = []
    for i in range(n):
        a.append(list(map(int, input().split())))
    
    NEG_INF = float('-inf')
    
    f = [[NEG_INF]*m for _ in range(n)]
    f[0][0] = a[0][0]
    for j in range(1, m):
        f[0][j] = f[0][j-1] + a[0][j]
    for i in range(1, n):
        f[i][0] = f[i-1][0] + a[i][0]
        for j in range(1, m):
            f[i][j] = max(f[i-1][j], f[i][j-1]) + a[i][j]
    
    g = [[NEG_INF]*m for _ in range(n)]
    g[n-1][m-1] = a[n-1][m-1]
    for j in range(m-2, -1, -1):
        g[n-1][j] = g[n-1][j+1] + a[n-1][j]
    for i in range(n-2, -1, -1):
        g[i][m-1] = g[i+1][m-1] + a[i][m-1]
        for j in range(m-2, -1, -1):
            g[i][j] = max(g[i+1][j], g[i][j+1]) + a[i][j]
    
    # diagonals d = i+j, 0 to n+m-2
    D = n+m-1
    max1 = [NEG_INF]*D
    max1_idx = [-1]*D  # use i as index (j determined)
    max2 = [NEG_INF]*D
    
    for i in range(n):
        for j in range(m):
            d = i+j
            h = f[i][j] + g[i][j] - a[i][j]
            if h > max1[d]:
                max2[d] = max1[d]
                max1[d] = h
                max1_idx[d] = i
            elif h > max2[d]:
                max2[d] = h
    
    ans = float('inf')
    for i in range(n):
        for j in range(m):
            d = i+j
            if max1_idx[d] == i:
                M1 = max2[d]
            else:
                M1 = max1[d]
            M2 = f[i][j] + g[i][j] - 3*a[i][j]
            new_max = max(M1, M2)
            if new_max < ans:
                ans = new_max
    
    print(ans)

t = int(input())
for _ in range(t):
    solve()
