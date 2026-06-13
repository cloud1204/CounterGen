import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    funcs = []
    for _ in range(n):
        a,b,c = map(int, input().split())
        funcs.append((a,b,c))
    
    order = sorted(range(n), key=lambda i: -funcs[i][2])
    
    def above(i, j):
        a1,b1,c1 = funcs[i]
        a2,b2,c2 = funcs[j]
        da = a1-a2
        db = b1-b2
        dc = c1-c2
        if da == 0:
            return db == 0 and dc > 0
        if da < 0:
            return False
        return db*db - 4*da*dc < 0
    
    dp_in = [1]*n
    dp_out = [1]*n
    
    for jj in range(n):
        j = order[jj]
        for ii in range(jj):
            i = order[ii]
            if above(i, j):
                if dp_in[i]+1 > dp_in[j]:
                    dp_in[j] = dp_in[i]+1
    
    for jj in range(n-1, -1, -1):
        i = order[jj]
        for kk in range(jj+1, n):
            j = order[kk]
            if above(i, j):
                if dp_out[j]+1 > dp_out[i]:
                    dp_out[i] = dp_out[j]+1
    
    ans = [dp_in[i]+dp_out[i]-1 for i in range(n)]
    print(*ans)

t = int(input())
for _ in range(t):
    solve()
