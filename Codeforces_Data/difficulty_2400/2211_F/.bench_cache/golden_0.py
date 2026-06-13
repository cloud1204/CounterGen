import sys
from sys import stdin

MOD = 676767677

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    
    # We need factorials up to max(n+m) for all test cases
    # But factorials are global; precompute up to 2*10^6 + 10
    MAXF = 2_000_010
    fact = [1]*(MAXF)
    for i in range(1, MAXF):
        fact[i] = fact[i-1]*i % MOD
    inv_fact = [1]*MAXF
    inv_fact[MAXF-1] = pow(fact[MAXF-1], MOD-2, MOD)
    for i in range(MAXF-2, -1, -1):
        inv_fact[i] = inv_fact[i+1]*(i+1) % MOD
    
    def C(n, k):
        if k < 0 or k > n or n < 0:
            return 0
        return fact[n]*inv_fact[k]%MOD*inv_fact[n-k]%MOD
    
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        m = int(input_data[idx]); idx+=1
        
        # Compute lb, rb, depth for each position
        lb = [0]*(n+1)
        rb = [0]*(n+1)
        dep = [0]*(n+1)
        stack = [(1, n, 1)]
        while stack:
            l, r, d = stack.pop()
            if l > r:
                continue
            mid = (l+r)//2
            lb[mid] = l
            rb[mid] = r
            dep[mid] = d
            stack.append((l, mid-1, d+1))
            stack.append((mid+1, r, d+1))
        
        total = 0
        for p in range(1, n+1):
            L = lb[p] - 1
            P = p
            R = rb[p] + 1
            
            T = C(m+n-1, n)
            sub1 = C(m+n+P-R-1, P+n-R) if R <= n else 0
            sub2 = C(m+n+L-P-1, L+n-P) if L >= 1 else 0
            add = C(m+n+L-R-1, L+n-R) if (L >= 1 and R <= n) else 0
            
            fp = (T - sub1 - sub2 + add) % MOD
            total = (total + dep[p] * fp) % MOD
        
        out.append(str(total % MOD))
    
    print('\n'.join(out))

solve()
