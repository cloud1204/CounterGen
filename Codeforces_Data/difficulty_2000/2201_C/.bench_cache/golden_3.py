import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 998244353
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        S = input_data[idx].decode(); idx += 1
        # 1-indexed
        P = [0] * (n+2)
        for i in range(1, n+1):
            P[i] = P[i-1] + (1 if S[i-1] == '(' else -1)
        # nxt[i]: smallest p >= i with P[p] < 2, for i in [1, n]
        nxt = [n+1] * (n+2)
        for i in range(n, 0, -1):
            if P[i] < 2:
                nxt[i] = i
            else:
                nxt[i] = nxt[i+1]
        # r(i) = nxt[i] - 1 for S_i = '('
        # BIT for suffix sum: we want sum at positions >= j, in range [1, n]
        # Use BIT for prefix sum, then suffix = total - prefix(j-1)
        bit = [0] * (n+2)
        def update(i, v):
            while i <= n+1:
                bit[i] = (bit[i] + v) % MOD
                i += i & -i
        def query(i):
            s = 0
            while i > 0:
                s = (s + bit[i]) % MOD
                i -= i & -i
            return s
        
        dp = [0] * (n+1)
        dp[0] = 1
        A = 1  # dp[0]
        total_bit = 0
        for j in range(1, n+1):
            if j >= 2:
                i = j - 1
                if S[i-1] == ')':
                    A = (A + dp[i]) % MOD
                else:  # '('
                    pos = nxt[i]  # r(i)+1 = nxt[i]
                    if pos >= 1 and pos <= n:
                        update(pos, dp[i])
                        total_bit = (total_bit + dp[i]) % MOD
                    # if pos > n, then r(i)+1 > n, meaning any j up to n is fine. Let's check.
                    # r(i)+1 might be n+1 (if nxt[i]=n+1). Then any j up to n is ≤ r(i)+1. Hmm.
                    # Suffix sum should include this. Let me put it at position n+1, then suffix sum from j ≤ n includes it.
                    elif pos == n+1:
                        update(n+1, dp[i])
                        total_bit = (total_bit + dp[i]) % MOD
            # B_j = suffix sum from j to n+1
            B = (total_bit - query(j-1)) % MOD
            dp[j] = (A + B) % MOD
        
        ans = 0
        pow2 = 1
        for j in range(1, n+1):
            if S[j-1] == '(':
                ans = (ans + pow2) % MOD
            else:
                ans = (ans + dp[j]) % MOD
            pow2 = pow2 * 2 % MOD
        results.append(ans)
    print('\n'.join(map(str, results)))

solve()
