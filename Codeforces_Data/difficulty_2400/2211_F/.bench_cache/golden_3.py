import sys
from sys import stdin

def solve():
    MOD = 676767677
    MAXN = 2_000_010
    fact = [1]*(MAXN+1)
    for i in range(1, MAXN+1):
        fact[i] = fact[i-1]*i % MOD
    inv_fact = [1]*(MAXN+1)
    inv_fact[MAXN] = pow(fact[MAXN], MOD-2, MOD)
    for i in range(MAXN-1, -1, -1):
        inv_fact[i] = inv_fact[i+1]*(i+1) % MOD
    
    def C(n, k):
        if k<0 or k>n or n<0:
            return 0
        return fact[n]*inv_fact[k]%MOD*inv_fact[n-k]%MOD
    
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        m = int(input_data[idx]); idx+=1
        
        # Compute for each p in 1..n: depth, qL, qR
        # Iterative stack
        ans = 0
        stack = [(1, n, 1, 0, 0)]  # l, r, depth, qL, qR
        while stack:
            l, r, d, qL, qR = stack.pop()
            if l > r:
                continue
            p = (l+r)//2
            # process p
            alpha = 1 if qL > 0 else 0
            beta = 1 if qR > 0 else 0
            S1 = C(m+n-1, n)
            S2 = C(m+qL+n-p-1, qL+n-p) if alpha else 0
            S3 = C(m+n+p-qR-1, n+p-qR) if beta else 0
            S4 = C(m+qL+n-qR-1, qL+n-qR) if (alpha and beta) else 0
            Np = (S1 - alpha*S2 - beta*S3 + alpha*beta*S4) % MOD
            ans = (ans + d*Np) % MOD
            # children
            # left child: range [l, p-1], depth d+1, new qR = p (since p > any in left), qL unchanged
            stack.append((l, p-1, d+1, qL, p))
            # right child: range [p+1, r], depth d+1, new qL = p, qR unchanged
            stack.append((p+1, r, d+1, p, qR))
        ans %= MOD
        out.append(str(ans))
    print('\n'.join(out))

solve()
