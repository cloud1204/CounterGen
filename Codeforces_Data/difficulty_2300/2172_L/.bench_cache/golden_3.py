def solve():
    import sys
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    m = int(input_data[1])
    k = int(input_data[2])
    s = input_data[3]
    
    NEG = -10**9
    total = [NEG] * (m + 1)
    total[0] = 0
    
    for r in range(k):
        positions = []
        p = r
        while p <= n - 1:
            positions.append(p)
            p += k
        if not positions:
            continue
        
        L = len(positions)
        has_var = [pos <= n - k for pos in positions]
        has_trans = [pos >= 1 for pos in positions]
        trans_val = []
        for pos in positions:
            if pos >= 1:
                trans_val.append(1 if s[pos] != s[pos-1] else 0)
            else:
                trans_val.append(0)
        
        max_vars = sum(has_var)
        cap = min(max_vars, m)
        
        dp = [[NEG, NEG] for _ in range(cap + 1)]
        dp[0][0] = 0
        
        for i in range(L):
            new_dp = [[NEG, NEG] for _ in range(cap + 1)]
            for used in range(cap + 1):
                for xp in range(2):
                    if dp[used][xp] == NEG:
                        continue
                    val = dp[used][xp]
                    for xc in range(2):
                        if xc == 1 and not has_var[i]:
                            continue
                        nu = used + xc
                        if nu > cap:
                            continue
                        contrib = 0
                        if has_trans[i]:
                            contrib = trans_val[i] ^ xp ^ xc
                        nv = val + contrib
                        if nv > new_dp[nu][xc]:
                            new_dp[nu][xc] = nv
            dp = new_dp
        
        g = [NEG] * (cap + 1)
        for used in range(cap + 1):
            g[used] = max(dp[used][0], dp[used][1])
        
        new_total = [NEG] * (m + 1)
        for j in range(m + 1):
            if total[j] == NEG:
                continue
            for u in range(min(cap, m - j) + 1):
                if g[u] == NEG:
                    continue
                v = total[j] + g[u]
                if v > new_total[j + u]:
                    new_total[j + u] = v
        total = new_total
    
    ans = 1 + max(total)
    print(ans)

solve()
