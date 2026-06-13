import sys
input = sys.stdin.readline

def solve():
    MOD = 998244353
    n = int(input())
    s = input().strip()
    P = [0]*(n+1)
    for i in range(1, n+1):
        P[i] = P[i-1] + (1 if s[i-1]=='(' else -1)
    next_lt2 = [n+1]*(n+2)
    for i in range(n, 0, -1):
        if P[i] <= 1:
            next_lt2[i] = i
        else:
            next_lt2[i] = next_lt2[i+1]
    delta = [0]*(n+3)
    A = 0
    closeSum = 0
    ans = 0
    pow2 = 1
    for p in range(1, n+1):
        A = (A + delta[p]) % MOD
        fp = (closeSum + A + 1) % MOD
        if s[p-1]==')':
            closeSum = (closeSum + fp) % MOD
            ans = (ans + fp) % MOD
        else:
            ans = (ans + pow2) % MOD
            Rp = next_lt2[p] - 1
            L = p+1
            Rr = Rp + 1
            if L <= Rr:
                delta[L] = (delta[L] + fp) % MOD
                delta[Rr+1] = (delta[Rr+1] - fp) % MOD
        pow2 = (pow2 * 2) % MOD
    print(ans % MOD)

t = int(input())
for _ in range(t):
    solve()
