import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    d = list(map(int, input().split()))
    A = [0]*n
    for i in range(n):
        for j in range(i+1, n):
            if p[j] > p[i]:
                A[i] += 1
    for i in range(n):
        if d[i] > A[i]:
            print(-1)
            return
    order = sorted(range(n), key=lambda x: -p[x])
    L = []
    for i in order:
        m = len(L)
        cnt = 0
        insert_pos = -1
        for k in range(m, -1, -1):
            if cnt == d[i]:
                insert_pos = k
                break
            if k > 0 and L[k-1] > i:
                cnt += 1
        if insert_pos == -1:
            print(-1)
            return
        L.insert(insert_pos, i)
    q = [0]*n
    for rank, pos in enumerate(L):
        q[pos] = rank + 1
    print(*q)

t = int(input())
for _ in range(t):
    solve()
