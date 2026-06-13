import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    MOD = 998244353
    maxL = [0] * n  # maxL[i] for i in 1..n-1, representing constraints with r-1 = i
    for _ in range(m):
        l, r = map(int, input().split())
        i = r - 1  # r-1 in t indexing
        if l > maxL[i]:
            maxL[i] = l
    
    # dp over t_1..t_{n-1}
    # A[j] for j in 0..n-1, A[0] = dp where no 1 yet
    A = [0] * n
    A[0] = 1  # initial: before any t, 0 ones, last-1 = 0
    S = 1
    threshold = 0
    ptr = 0  # positions before ptr have been zeroed
    
    for i in range(1, n):  # i is t_i index, from 1 to n-1
        # New A[i] = S (after we add t_i = 1)
        new_val = S
        # Apply maxL[i]: zero out A[j] for j < maxL[i]
        new_threshold = max(threshold, maxL[i])
        while ptr < new_threshold:
            S = (S - A[ptr]) % MOD
            A[ptr] = 0
            ptr += 1
        threshold = new_threshold
        A[i] = new_val
        S = (S + new_val) % MOD
    
    # Final: need all constraints satisfied; since we processed maxL[i] for all i = r-1, all are handled
    ans = (2 * S) % MOD
    print(ans % MOD)

t = int(input())
for _ in range(t):
    solve()
