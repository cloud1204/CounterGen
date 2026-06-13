def solve():
    n = int(input())
    p = list(map(int, input().split()))
    d = list(map(int, input().split()))
    
    q = [0] * n
    unassigned = set(range(n))
    
    for k in range(1, n+1):
        ready = []
        for i in unassigned:
            cnt = sum(1 for j in unassigned if j > i and p[j] > p[i])
            if cnt == d[i]:
                ready.append(i)
        if not ready:
            print(-1)
            return
        chosen = -1
        for i in ready:
            ok = True
            for j in ready:
                if j > i and p[j] > p[i]:
                    ok = False
                    break
            if ok:
                chosen = i
                break
        if chosen == -1:
            print(-1)
            return
        q[chosen] = k
        unassigned.remove(chosen)
    
    print(*q)

t = int(input())
for _ in range(t):
    solve()
