import sys
from sys import setrecursionlimit

MOD = 676767677
MAX = 2_200_000

# precompute factorials
fact = [1]*(MAX+1)
for i in range(1, MAX+1):
    fact[i] = fact[i-1]*i % MOD
inv_fact = [1]*(MAX+1)
inv_fact[MAX] = pow(fact[MAX], MOD-2, MOD)
for i in range(MAX, 0, -1):
    inv_fact[i-1] = inv_fact[i]*i % MOD

def C(n, k):
    if k < 0 or k > n or n < 0:
        return 0
    return fact[n]*inv_fact[k]%MOD*inv_fact[n-k]%MOD
