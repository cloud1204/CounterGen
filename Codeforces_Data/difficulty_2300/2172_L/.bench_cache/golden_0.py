def solve():
    import sys
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    m = int(input_data[1])
    k = int(input_data[2])
    s = input_data[3]
    
    # boundaries: b[i] = 1 if s[i] != s[i+1], for i in 0..n-2
    b = [1 if s[i] != s[i+1] else 0 for i in range(n-1)]
    
    if n == 1:
        print(1)
        return
    
    # For each residue r in 0..k-1, build chain
    # x positions: r, r+k, ... ≤ n-k
    # b positions: r-1 (if r≥1), r+k-1, r+2k-1, ... ≤ n-2
    
    chains = []
    for r in range(k):
        chain = []  # list of ('x', idx) or ('b', value)
        if r >= 1:
            chain.append(('b', b[r-1]))
        l = r
        while l <= n - k:
            chain.append(('x', l))
            bi = l + k - 1
            if bi <= n - 2:
                chain.append(('b', b[bi]))
            l += k
        chains.append(chain)
    
    # For each chain, compute best[j] = max boundaries-set-to-1 with j x's chosen
    chain_bests = []
    for chain in chains:
        x_count = sum(1 for e in chain if e[0] == 'x')
        b_count = sum(1 for e in chain if e[0] == 'b')
        if x_count == 0:
            # all boundaries unchanged
            score = sum(e[1] for e in chain if e[0] == 'b')
            chain_bests.append([score])
            continue
        
        # DP: dp[j][prev] = max score (boundaries set to 1 so far that have been finalized)
        # prev ∈ {0, 1}, value of last x in chain (default 0 if no x yet, but we need to handle initial case)
        # initial: before any element, prev = 0 (no x yet), j = 0, score = 0
        # But there might be a b at the start with no x before it. So we need to handle b's properly.
        
        # State: after processing element i, dp[j][prev] where prev is last x value (or "no x yet")
        # Pending: if last element processed was a b, it hasn't been finalized yet.
        # Let's encode state more carefully.
        
        # Reformulate: scan chain. Keep state (j, prev_x_val, pending_b_val) where pending_b_val is the un-finalized b (None if none pending). When we hit an x, finalize pending b. At end, finalize any remaining pending b.
        
        # Actually pending b is at most 1 (since x and b alternate). Let me track: pending_b = initial b value of pending boundary that's been XORed with prev_x already; or None.
        
        # Hmm let me think again. A boundary b_i's final value = b_i_initial XOR x_left XOR x_right.
        # When processing chain, when we encounter a b, we know x_left already (it's prev_x). We can XOR. Then store as "pending", to be XORed with x_right when next x comes.
        # If no next x (end of chain), finalize as is.
        # If b has no left x (i.e., b is the first element), x_left doesn't exist. We just store initial value.
        
        # State: (j, prev_x, pending) where pending is the partial value (None if no pending).
        
        # Let's just do it with full state tracking.
        
        INF = float('-inf')
        # dp[j][prev][pending] where prev ∈ {0,1,2} (2=no x yet), pending ∈ {0, 1, 2} (2 = no pending)
        # Actually let's just use dict
        
        # Start: j=0, prev=2 (no x), pending=2 (none), score=0
        dp = {(0, 2, 2): 0}
        
        for elem in chain:
            new_dp = {}
            if elem[0] == 'x':
                xi = elem[1]
                for (j, prev, pending), score in dp.items():
                    for xv in [0, 1]:
                        nj = j + (1 if xv == 1 else 0)
                        # Finalize pending if exists
                        if pending != 2:
                            final_b = pending ^ xv
                            ns = score + final_b
                        else:
                            ns = score
                        nprev = xv
                        npending = 2
                        key = (nj, nprev, npending)
                        if key not in new_dp or new_dp[key] < ns:
                            new_dp[key] = ns
            else:  # 'b'
                bv = elem[1]
                for (j, prev, pending), score in dp.items():
                    # Shouldn't have pending already (alternating)
                    # Compute partial: if prev exists, XOR with prev
                    if prev != 2:
                        partial = bv ^ prev
                    else:
                        partial = bv
                    key = (j, prev, partial)
                    if key not in new_dp or new_dp[key] < score:
                        new_dp[key] = score
            dp = new_dp
        
        # At end, finalize any pending b
        best = [INF] * (x_count + 1)
        for (j, prev, pending), score in dp.items():
            if pending != 2:
                score += pending
            if 0 <= j <= x_count:
                if best[j] < score:
                    best[j] = score
        
        chain_bests.append(best)
    
    # Knapsack: combine all chain_bests with total j ≤ m
    INF = float('-inf')
    dp = [INF] * (m + 1)
    dp[0] = 0
    for best in chain_bests:
        new_dp = [INF] * (m + 1)
        for j in range(m + 1):
            if dp[j] == INF:
                continue
            for jc in range(len(best)):
                if best[jc] == INF:
                    continue
                nj = j + jc
                if nj > m:
                    break
                if new_dp[nj] < dp[j] + best[jc]:
                    new_dp[nj] = dp[j] + best[jc]
        dp = new_dp
    
    ans = max(dp[j] for j in range(m + 1) if dp[j] != INF)
    print(ans + 1)

solve()
