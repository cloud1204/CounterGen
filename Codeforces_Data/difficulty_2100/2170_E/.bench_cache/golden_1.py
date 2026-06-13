import sys
from sys import stdin

def solve():
    input = stdin.readline
    MOD = 998244353
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        N = n - 1
        maxL = [0] * (N + 2)
        for _ in range(m):
            l, r = map(int, input().split())
            # constraint d_l .. d_{r-1}
            dl, dr = l, r - 1
            if maxL[dr] < dl:
                maxL[dr] = dl
        
        # Fenwick tree size N+1 (indices 0..N)
        size = N + 2
        bit = [0] * (size + 1)
        def update(i, v):
            i += 1
            while i <= size:
                bit[i] = (bit[i] + v) % MOD
                i += i & -i
        def query(i):
            # prefix sum [0..i]
            i += 1
            s = 0
            while i > 0:
                s = (s + bit[i]) % MOD
                i -= i & -i
            return s
        
        update(0, 1)  # A[0] = 1
        minIdx = 0
        
        for i in range(1, N + 1):
            # total = sum A[minIdx..i-1]
            total = (query(i - 1) - (query(minIdx - 1) if minIdx > 0 else 0)) % MOD
            update(i, total)
            if maxL[i] > minIdx:
                minIdx = maxL[i]
        
        ans = (query(N) - (query(minIdx - 1) if minIdx > 0 else 0)) % MOD
        ans = ans * 2 % MOD
        out.append(str(ans))
    
    print('\n'.join(out))

solve()
