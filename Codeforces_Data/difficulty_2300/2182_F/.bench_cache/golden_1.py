from collections import defaultdict
MOD = 998244353

def solve_query(cnt, x):
    n_total = sum(cnt)
    # dp[j][cap] = ways
    dp = defaultdict(int)
    dp[(0, 0)] = 1
    answered = 0  # ways with cap >= x
    
    for v in range(60, -1, -1):
        c = cnt[v]
        if c == 0:
            continue
        new_dp = defaultdict(int)
        # precompute C(c, k)
        binom = [1] * (c+1)
        for i in range(1, c+1):
            binom[i] = binom[i-1] * (c - i + 1) // i
        
        for (j, cap), ways in dp.items():
            for k in range(0, c+1):
                # pick k reindeer at value v, positions j+1..j+k
                contrib = 0
                for t in range(1, k+1):
                    pos = j + t
                    if v >= pos - 1:
                        contrib += 1 << (v - (pos-1))
                new_cap = cap + contrib
                new_j = min(j + k, 62)
                w = ways * binom[k] % MOD
                if new_cap >= x:
                    # remaining values contribute and we want to count all subsets of remaining reindeer
                    # but we still need to multiply by future free choices. We can't finalize here unless we know total remaining.
                    # Just keep capped cap = x (marker for "done")
                    new_dp[(new_j, x)] = (new_dp[(new_j, x)] + w) % MOD
                else:
                    new_dp[(new_j, new_cap)] = (new_dp[(new_j, new_cap)] + w) % MOD
        dp = new_dp
    
    ans = 0
    for (j, cap), ways in dp.items():
        if cap >= x:
            ans = (ans + ways) % MOD
    return ans
