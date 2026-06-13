import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    funcs = []
    for _ in range(n):
        a, b, c = map(int, input().split())
        funcs.append((a, b, c))
    
    below = [[False]*n for _ in range(n)]
    for i in range(n):
        ai, bi, ci = funcs[i]
        for j in range(n):
            if i == j: continue
            aj, bj, cj = funcs[j]
            da = ai - aj
            db = bi - bj
            dc = ci - cj
            if da == 0 and db == 0:
                if dc < 0:
                    below[i][j] = True
            elif da == 0:
                pass
            else:
                disc = db*db - 4*da*dc
                if disc < 0:
                    if dc < 0:
                        below[i][j] = True
    
    order = sorted(range(n), key=lambda i: funcs[i][2])
    down = [1]*n
    pos = {v:k for k,v in enumerate(order)}
    for k, i in enumerate(order):
        for kk in range(k):
            j = order[kk]
            if below[j][i]:
                if down[j]+1 > down[i]:
                    down[i] = down[j]+1
    
    up = [1]*n
    for k in range(n-1, -1, -1):
        i = order[k]
        for kk in range(k+1, n):
            j = order[kk]
            if below[i][j]:
                if up[j]+1 > up[i]:
                    up[i] = up[j]+1
    
    ans = [down[i]+up[i]-1 for i in range(n)]
    print(*ans)
