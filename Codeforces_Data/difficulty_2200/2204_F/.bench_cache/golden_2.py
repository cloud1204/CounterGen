import sys
from sys import stdin

def solve():
    MOD = 998244353
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(input_data[idx]); idx+=1
    m = int(input_data[idx]); idx+=1
    a = [int(input_data[idx+i]) for i in range(n)]; idx+=n
    ks = [int(input_data[idx+i]) for i in range(m)]; idx+=m
    
    # Compute cnt_i: number of subarrays where a_i is min (with tiebreak: leftmost equal is min)
    # L[i]: leftmost index such that all a[L..i] >= a[i], and a[L-1] < a[i] (strict on left)
    # R[i]: rightmost index such that all a[i..R] > a[i], and a[R+1] <= a[i] (non-strict on right)
    # cnt_i = (i - L + 1) * (R - i + 1)
    
    L = [0]*n
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        L[i] = stack[-1]+1 if stack else 0
        stack.append(i)
    
    R = [0]*n
    stack = []
    for i in range(n-1, -1, -1):
        while stack and a[stack[-1]] > a[i]:
            stack.pop()
        R[i] = stack[-1]-1 if stack else n-1
        stack.append(i)
    
    # T1 = sum_i (i+1)*(n-i) * inv(a_i)   (0-indexed: i goes 0..n-1, subarrays containing i = (i+1)*(n-i))
    T1 = 0
    T2 = 0
    cnt = [0]*n
    inv_a = [pow(a[i], MOD-2, MOD) for i in range(n)]
    for i in range(n):
        c = (i - L[i] + 1) * (R[i] - i + 1)
        cnt[i] = c % MOD
        T1 = (T1 + (i+1)*(n-i) % MOD * inv_a[i]) % MOD
        T2 = (T2 + cnt[i] * inv_a[i]) % MOD
    
    out = []
    base = (T1 - T2) % MOD
    for k in ks:
        T3 = 0
        for i in range(n):
            if a[i] <= k+1:
                T3 = (T3 + cnt[i] * ((k - a[i] + 2) % MOD)) % MOD
            else:
                T3 = (T3 + cnt[i] * pow(a[i]-k, MOD-2, MOD)) % MOD
        ans = (base + T3) % MOD
        out.append(ans)
    
    sys.stdout.write('\n'.join(map(str, out)))

solve()
