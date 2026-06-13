import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    d = list(map(int, input().split()))
    
    a = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if p[j] > p[i]:
                a[i] += 1
    
    for i in range(n):
        if d[i] > a[i] or d[i] < 0:
            print(-1)
            return
    
    order = sorted(range(n), key=lambda x: -p[x])
    
    S = []
    
    for idx in order:
        R_flags = [1 if S[k] > idx else 0 for k in range(len(S))]
        suffix_R = [0] * (len(S) + 1)
        for k in range(len(S) - 1, -1, -1):
            suffix_R[k] = suffix_R[k + 1] + R_flags[k]
        
        pos = -1
        for k in range(len(S) + 1):
            if suffix_R[k] == d[idx]:
                pos = k
                break
        
        if pos == -1:
            print(-1)
            return
        
        S.insert(pos, idx)
    
    q = [0] * n
    for rank, idx in enumerate(S):
        q[idx] = rank + 1
    
    print(*q)

t = int(input())
for _ in range(t):
    solve()
