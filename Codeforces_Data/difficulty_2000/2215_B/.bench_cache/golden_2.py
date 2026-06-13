import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    d = list(map(int, input().split()))
    c = [0]*n
    for i in range(n):
        for j in range(i+1, n):
            if p[j] > p[i]:
                c[i] += 1
    q = [0]*n
    placed = [False]*n
    for k in range(1, n+1):
        chosen = -1
        for i in range(n):
            if not placed[i] and c[i] == d[i]:
                chosen = i
                break
        if chosen == -1:
            print(-1)
            return
        placed[chosen] = True
        q[chosen] = k
        for j in range(chosen):
            if not placed[j] and p[j] < p[chosen]:
                c[j] -= 1
                if c[j] < d[j]:
                    pass
    print(*q)

t = int(input())
for _ in range(t):
    solve()
