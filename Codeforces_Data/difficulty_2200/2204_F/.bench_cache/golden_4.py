import sys
from sys import stdin

def solve():
    MOD = 998244353
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1
    a = [int(input_data[idx+i]) for i in range(n)]; idx += n
    ks = [int(input_data[idx+i]) for i in range(m)]; idx += m
    
    # compute count[i]: 0-indexed
    left = [-1]*n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    right = [n]*n
    stack = []
    for i in range(n-1, -1, -1):
        while stack and a[stack[-1]] > a[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    count = [(i - left[i]) * (right[i] - i) for i in range(n)]
    
    # T1
    T1 = 0
    for i in range(n):
        inv_a = pow(a[i], MOD-2, MOD)
        T1 = (T1 + inv_a * (i+1) * (n - i)) % MOD
    
    # precompute inv_a_i
    inv_a = [pow(a[i], MOD-2, MOD) for i in range(n)]
    
    out = []
    for k in ks:
        T2 = 0
        for i in range(n):
            v = a[i]
            c = count[i]
            if k >= v - 1:
                # h = (k - v + 2) - 1/v
                h = (k - v + 2 - inv_a[i]) % MOD
            else:
                # h = 1/(v-k) - 1/v
                h = (pow(v - k, MOD-2, MOD) - inv_a[i]) % MOD
            T2 = (T2 + c * h) % MOD
        ans = (T1 + T2) % MOD
        out.append(ans)
    
    sys.stdout.write('\n'.join(map(str, out)))

solve()
