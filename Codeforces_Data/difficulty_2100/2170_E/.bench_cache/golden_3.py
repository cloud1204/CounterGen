import sys
input = sys.stdin.readline

def solve():
    MOD = 998244353
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        L = n - 1
        req = [0] * (L + 1)
        for _ in range(m):
            l, r = map(int, input().split())
            idx = r - 1
            if l > req[idx]:
                req[idx] = l
        for i in range(1, L + 1):
            if req[i-1] > req[i]:
                req[i] = req[i-1]
        S = [0] * (L + 1)
        P = [0] * (L + 1)
        S[0] = 1
        P[0] = 1
        for i in range(1, L + 1):
            if req[i] == 0:
                S[i] = (1 + P[i-1]) % MOD
            else:
                a = P[i-1]
                b = P[req[i]-2] if req[i] - 2 >= 0 else 0
                S[i] = (a - b) % MOD
            P[i] = (P[i-1] + S[i]) % MOD
        ans = (2 * S[L]) % MOD
        out.append(str(ans))
    sys.stdout.write('\n'.join(out) + '\n')

solve()
