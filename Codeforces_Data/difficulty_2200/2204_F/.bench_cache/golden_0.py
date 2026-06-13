import sys
from sys import stdin

def solve():
    MOD = 998244353
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    n, m = int(input_data[idx]), int(input_data[idx+1])
    idx += 2
    a = [int(input_data[idx+i]) for i in range(n)]
    idx += n
    ks = [int(input_data[idx+i]) for i in range(m)]
    
    # Compute counts: for each j, number of subarrays where a[j] is min
    # Use strict less on left, less-or-equal on right (or similar)
    left = [0]*n  # index of previous strictly smaller
    stack = []
    for i in range(n):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    right = [0]*n  # index of next smaller (strictly)
    stack = []
    for i in range(n-1, -1, -1):
        while stack and a[stack[-1]] > a[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    count = [(i - left[i]) * (right[i] - i) for i in range(n)]
    
    # base = sum over subarrays of sum 1/a_j = sum_j (j+1)*(n-j) * (1/a_j)
    base = 0
    inv_a = [pow(a[i], MOD-2, MOD) for i in range(n)]
    for i in range(n):
        base = (base + (i+1)*(n-i) % MOD * inv_a[i]) % MOD
    
    results = []
    for k in ks:
        # ans = base + sum_j count_j * g(a_j, k)
        total = base
        for i in range(n):
            b = a[i]
            if k <= b - 1:
                # g = k / (b*(b-k))
                if k == 0:
                    g = 0
                else:
                    g = k * pow(b * (b - k) % MOD, MOD-2, MOD) % MOD
            else:
                # g = k + 2 - b - 1/b
                g = (k + 2 - b) % MOD
                g = (g - inv_a[i]) % MOD
            total = (total + count[i] * g) % MOD
        results.append(total % MOD)
    
    sys.stdout.write('\n'.join(str(x) for x in results) + '\n')

solve()
