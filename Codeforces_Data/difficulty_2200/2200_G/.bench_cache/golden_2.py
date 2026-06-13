import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(a, m=MOD):
    return pow(a, m-2, m)

def solve():
    n, x = map(int, input().split())
    ops = input().split()
    mults = []
    adds = []
    for op in ops:
        sym = op[0]
        y = int(op[1:])
        if sym == '+':
            adds.append(y % MOD)
        elif sym == '-':
            adds.append((-y) % MOD)
        elif sym == 'x':
            mults.append(y % MOD)
        else:
            mults.append(modinv(y % MOD))
    
    k = len(mults)
    e = [0] * (k + 1)
    e[0] = 1
    for i, m in enumerate(mults):
        for s in range(i+1, 0, -1):
            e[s] = (e[s] + e[s-1] * m) % MOD
    
    prod_m = 1
    for m in mults:
        prod_m = prod_m * m % MOD
    
    fact = [1] * (k + 2)
    for i in range(1, k + 2):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (k + 2)
    inv_fact[k+1] = modinv(fact[k+1])
    for i in range(k, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
    
    def binom(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD
    
    C = 0
    for s in range(k + 1):
        C = (C + e[s] * modinv(binom(k, s))) % MOD
    C = C * modinv(k + 1) % MOD
    
    sum_a = sum(adds) % MOD
    
    ans = (x % MOD) * prod_m % MOD
    ans = (ans + C * sum_a) % MOD
    print(ans)

t = int(input())
for _ in range(t):
    solve()
