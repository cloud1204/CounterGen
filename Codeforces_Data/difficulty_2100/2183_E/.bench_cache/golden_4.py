import sys
from math import gcd
from fractions import Fraction
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    # Check fixed values are strictly increasing-compatible
    # Brute force fill positions in order
    
    count = 0
    def dfs(i, prev):
        nonlocal count
        if i == n:
            # check sum
            s = Fraction(0)
            for j in range(n):
                k = (j+1) % n
                x, y = a[j], a[k]
                l = x*y//gcd(x,y)
                s += Fraction(1, l)
            if s >= 1:
                count += 1
            return
        if a[i] != 0:
            if a[i] > prev and a[i] <= m - (n-1-i):
                dfs(i+1, a[i])
        else:
            # need a[i] in (prev, m - (n-1-i)]
            lo = prev + 1
            hi = m - (n-1-i)
            for v in range(lo, hi+1):
                a[i] = v
                dfs(i+1, v)
            a[i] = 0
    
    dfs(0, 0)
    print(count % MOD)

t = int(input())
for _ in range(t):
    solve()
