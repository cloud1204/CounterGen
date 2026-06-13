import sys
input=sys.stdin.readline

def solve():
    n=int(input())
    p=list(map(int,input().split()))
    d=list(map(int,input().split()))
    counts=[0]*n
    assigned=[False]*n
    q=[0]*n
    for v in range(n,0,-1):
        best=-1
        for i in range(n):
            if not assigned[i] and counts[i]==d[i]:
                if best==-1 or p[i]<p[best]:
                    best=i
        if best==-1:
            print(-1)
            return
        q[best]=v
        assigned[best]=True
        for i in range(best):
            if not assigned[i] and p[i]<p[best]:
                counts[i]+=1
    for i in range(n):
        if counts[i]!=d[i]:
            print(-1)
            return
    print(*q)

t=int(input())
for _ in range(t):
    solve()
