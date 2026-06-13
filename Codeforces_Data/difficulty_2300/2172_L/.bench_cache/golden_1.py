def solve():
    import sys
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    m = int(input_data[1])
    k = int(input_data[2])
    s = input_data[3]
    
    # boundaries b[i] for i=1..n-1
    b = [0] * (n + 1)
    for i in range(1, n):
        if s[i] != s[i-1]:
            b[i] = 1
    
    # nodes are 0..n, real boundary if 1<=i<=n-1
    # chains: residues r = 0..min(k-1, n)
    # For r in 0..k-1, chain = [r, r+k, r+2k, ...] while <= n
    
    NEG = -10**9
    # global knapsack: best[c] = max total value using c operations
    best = [NEG] * (m + 1)
    best[0] = 0
    
    for r in range(k):
        chain = []
        v = r
        while v <= n:
            chain.append(v)
            v += k
        L = len(chain)  # L = t+1
        t = L - 1  # number of edges
        
        # dp[z][c] = max value
        # start j=0, z_0=0, c=0, no nodes counted
        # we'll iterate deciding z_{j+1} for j=0..t-1, then close with z_{t+1}=0
        
        # state after deciding z_j: dp[z_j][c]
        INF_NEG = -10**9
        dp = [[INF_NEG] * (t + 2) for _ in range(2)]
        dp[0][0] = 0  # z_0 = 0, c=0
        
        for j in range(t):
            new_dp = [[INF_NEG] * (t + 2) for _ in range(2)]
            vj = chain[j]
            real = (1 <= vj <= n - 1)
            for z_prev in range(2):
                for c in range(t + 1):
                    if dp[z_prev][c] == INF_NEG:
                        continue
                    val = dp[z_prev][c]
                    for z_next in range(2):
                        toggle = z_prev ^ z_next
                        add = 0
                        if real:
                            add = b[vj] ^ toggle
                        nc = c + z_next
                        if nc > t:
                            continue
                        nv = val + add
                        if nv > new_dp[z_next][nc]:
                            new_dp[z_next][nc] = nv
            dp = new_dp
        
        # close: j=t, v_t = chain[t], z_{t+1}=0, toggle = z_t
        f = [INF_NEG] * (t + 2)
        vt = chain[t]
        real = (1 <= vt <= n - 1)
        for z_prev in range(2):
            for c in range(t + 1):
                if dp[z_prev][c] == INF_NEG:
                    continue
                val = dp[z_prev][c]
                toggle = z_prev
                add = 0
                if real:
                    add = b[vt] ^ toggle
                nv = val + add
                if nv > f[c]:
                    f[c] = nv
        
        # knapsack combine
        new_best = [NEG] * (m + 1)
        for c1 in range(m + 1):
            if best[c1] == NEG:
                continue
            for c2 in range(t + 1):
                if f[c2] == INF_NEG:
                    continue
                if c1 + c2 > m:
                    break
                v = best[c1] + f[c2]
                if v > new_best[c1 + c2]:
                    new_best[c1 + c2] = v
        best = new_best
    
    ans = max(best)
    print(1 + ans)

solve()
