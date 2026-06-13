import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, x = map(int, input().split())
    ops = input().split()
    mults = []
    adds = []
    for op in ops:
        c = op[0]
        y = int(op[1:])
        if c == 'x':
            mults.append(y % MOD)
        elif c == '/':
            mults.append(pow(y % MOD, MOD-2, MOD))
        elif c == '+':
            adds.append(y % MOD)
        else:
            adds.append((-y) % MOD)
    
    b = len(mults)
    e = [0]*(b+1)
    e[0] = 1
    for m in mults:
        for k in range(b, 0, -1):
            e[k] = (e[k] + e[k-1]*m) % MOD
    
    fact = [1]*(b+1)
    for i in range(1, b+1):
        fact[i] = fact[i-1]*i % MOD
    inv_fact = [1]*(b+1)
    inv_fact[b] = pow(fact[b], MOD-2, MOD)
    for i in range(b-1, -1, -1):
        inv_fact[i] = inv_fact[i+1]*(i+1) % MOD
    
    A = 0
    for k in range(b+1):
        Cbk = fact[b]*inv_fact[k]%MOD*inv_fact[b-k]%MOD
        A = (A + e[k]*pow(Cbk, MOD-2, MOD)) % MOD
    A = A * pow(b+1, MOD-2, MOD) % MOD
    
    M = e[b]
    v_sum = sum(adds) % MOD
    ans = (x % MOD * M + A * v_sum) % MOD
    print(ans)

t = int(input())
for _ in range(t):
    solve()
