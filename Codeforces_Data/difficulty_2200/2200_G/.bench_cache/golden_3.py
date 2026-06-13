import sys
input = sys.stdin.readline

MOD = 10**9 + 7

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
            mults.append(pow(y % MOD, MOD-2, MOD))
    K = len(mults)
    S = [0]*(K+1)
    S[0] = 1
    for m in mults:
        for k in range(K, 0, -1):
            S[k] = (S[k] + S[k-1]*m) % MOD
    P = S[K]
    fact = [1]*(K+1)
    for i in range(1, K+1):
        fact[i] = fact[i-1]*i % MOD
    inv_fact = [1]*(K+1)
    inv_fact[K] = pow(fact[K], MOD-2, MOD)
    for i in range(K, 0, -1):
        inv_fact[i-1] = inv_fact[i]*i % MOD
    C_val = 0
    for k in range(K+1):
        binom = fact[K]*inv_fact[k]%MOD*inv_fact[K-k]%MOD
        C_val = (C_val + S[k]*pow(binom, MOD-2, MOD)) % MOD
    C_val = C_val * pow(K+1, MOD-2, MOD) % MOD
    A_sum = sum(adds) % MOD
    ans = (x % MOD * P + C_val * A_sum) % MOD
    print(ans)

t = int(input())
for _ in range(t):
    solve()
