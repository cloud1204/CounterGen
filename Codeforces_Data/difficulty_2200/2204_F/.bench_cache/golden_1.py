import sys
input = sys.stdin.readline

def solve():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    idx = 0
    n, m = int(data[idx]), int(data[idx+1]); idx+=2
    a = [int(data[idx+i]) for i in range(n)]; idx+=n
    ks = [int(data[idx+i]) for i in range(m)]; idx+=m
    
    # prev less (strict)
    P = [-1]*n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        P[i] = stack[-1] if stack else -1
        stack.append(i)
    
    # next less or equal
    N = [n]*n
    stack = []
    for i in range(n-1,-1,-1):
        while stack and a[stack[-1]] > a[i]:
            stack.pop()
        N[i] = stack[-1] if stack else n
        stack.append(i)
    
    # cnt[v] = sum over i with a[i]=v of (i-P[i])*(N[i]-i)
    cnt = {}
    for i in range(n):
        c = (i - P[i]) * (N[i] - i)
        cnt[a[i]] = cnt.get(a[i], 0) + c
    
    # S = sum_i (i+1)*(n-i) * inv(a[i])
    S = 0
    for i in range(n):
        S = (S + (i+1)*(n-i) % MOD * pow(a[i], MOD-2, MOD)) % MOD
    
    # C = sum_v cnt[v] * inv(v)
    C = 0
    inv_v = {}
    for v, c in cnt.items():
        iv = pow(v, MOD-2, MOD)
        inv_v[v] = iv
        C = (C + c % MOD * iv) % MOD
    
    # Sort distinct v
    sorted_v = sorted(cnt.keys())
    
    # Initially all in "above": s1 = sum cnt[v]*inv(v) = C
    s1 = C
    s2 = 0
    s3 = 0
    ptr = 0
    
    out = []
    for k in ks:
        # move v with v <= k+1 to below
        while ptr < len(sorted_v) and sorted_v[ptr] <= k+1:
            v = sorted_v[ptr]
            c = cnt[v]
            s1 = (s1 - c % MOD * inv_v[v]) % MOD
            s2 = (s2 + c) % MOD
            s3 = (s3 + c % MOD * v) % MOD
            ptr += 1
        # T(k) = (1+k)*s1 + (k+2)*s2 - s3 - C
        T = ((1+k) % MOD * s1 + (k+2) % MOD * s2 - s3 - C) % MOD
        ans = (S + T) % MOD
        out.append(ans)
    
    sys.stdout.write('\n'.join(str(x % MOD) for x in out))

solve()
