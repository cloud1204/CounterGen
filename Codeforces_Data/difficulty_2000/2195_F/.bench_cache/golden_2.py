import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    fns = []
    for _ in range(n):
        a,b,c = map(int, input().split())
        fns.append((a,b,c))
    # s_i = a+c, w=b, t=a-c
    # edge i->j iff s_i<s_j and independent
    # independent iff (a_i!=a_j and 4(a_i-a_j)(c_i-c_j)>(b_i-b_j)^2)
    #                  or (a_i==a_j and b_i==b_j)
    
    idx = sorted(range(n), key=lambda i: (fns[i][0]+fns[i][2], i))
    # Reindex: process in order of s
    # But we need answer per original index.
    
    # forward[i]: longest path ending at i (number of nodes)
    forward = [1]*n
    for pos_j in range(n):
        j = idx[pos_j]
        aj,bj,cj = fns[j]
        sj = aj+cj
        best = 0
        for pos_i in range(pos_j):
            i = idx[pos_i]
            ai,bi,ci = fns[i]
            si = ai+ci
            if si >= sj: continue
            # check edge
            da = ai-aj; db = bi-bj; dc = ci-cj
            if da != 0:
                if 4*da*dc > db*db:
                    if forward[i] > best: best = forward[i]
            else:
                if db == 0:
                    if forward[i] > best: best = forward[i]
        forward[j] = best+1
    
    backward = [1]*n
    for pos_i in range(n-1,-1,-1):
        i = idx[pos_i]
        ai,bi,ci = fns[i]
        si = ai+ci
        best = 0
        for pos_j in range(pos_i+1,n):
            j = idx[pos_j]
            aj,bj,cj = fns[j]
            sj = aj+cj
            if sj <= si: continue
            da = ai-aj; db = bi-bj; dc = ci-cj
            if da != 0:
                if 4*da*dc > db*db:
                    if backward[j] > best: best = backward[j]
            else:
                if db == 0:
                    if backward[j] > best: best = backward[j]
        backward[i] = best+1
    
    ans = [forward[i]+backward[i]-1 for i in range(n)]
    print(*ans)

t = int(input())
for _ in range(t):
    solve()
