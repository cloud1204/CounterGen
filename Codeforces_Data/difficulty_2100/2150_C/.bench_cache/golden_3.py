def solve(n, v, a, b):
    posB = [0] * (n + 2)
    posA = [0] * (n + 2)
    for idx in range(n):
        posB[b[idx]] = idx + 1
        posA[a[idx]] = idx + 1
    
    # c[i] = posB[a[i-1]] for i in 1..n
    # i, j are 1-indexed
    
    # next_i[i][j] = smallest l > i with c_l >= j
    # Precompute or compute on the fly?
    
    # DP: dp[i][j] = max Alice value reaching (i, j)
    # Transitions from (i, j):
    # 1. Alice moves (if i <= n and c_i >= j):
    #    new value = dp[i][j] + v[a[i-1] - 1]
    #    Compute new (i', j').
    # 2. Bob moves (if j <= n and posA[b_j] >= i):
    #    new value = dp[i][j]
    #    Compute new (i', j').
    
    # End: when no more moves possible.
    
    ans = 0
    dp = {}
    dp[(1, 1)] = 0
    # BFS or topological
    # All states (i, j) can be reached, but transitions only forward.
    # Order by i + j.
    
    # Just iterate in order of (i + j), no wait state space is messy.
    # Use BFS, but with relaxation (max).
    
    from heapq import heappush, heappop
    # Or just iterate.
    
    # Simpler: queue.
    from collections import deque
    queue = deque([(1, 1)])
    in_queue = {(1, 1)}
    
    while queue:
        (i, j) = queue.popleft()
        in_queue.discard((i, j))
        cur = dp[(i, j)]
        
        # Alice move
        if i <= n and posB[a[i-1]] >= j:
            ai = a[i-1]
            new_val = cur + v[ai - 1]
            # New state
            # New i: smallest l > i with c_l >= new_j
            # But new_j depends.
            ci = posB[ai]
            if ci == j:
                # a_i = b_j, both advance
                new_j = j + 1
                # advance j' if needed (b_{new_j} in T)
                # But T = {a_1..a_i} ∪ {b_1..b_{j-1}}.
                # new_j should be smallest m > j with b_m ∉ T = posA[b_m] > i.
                # But i is current (before advance). After we take a_i, new i is i+1 or more.
                # Let's first advance i' to next l > i with c_l >= j'.
                # Then ensure j' is valid for new i.
                pass
            else:
                new_j = j
            # OK let me think more carefully
            # After Alice takes a_i: T' = T ∪ {a_i}
            # New Alice's pointer: smallest l > i with a_l ∉ T'.
            #   a_l ∉ T' for l > i iff a_l ∉ {b_1..b_{j-1}} ∪ {a_i}. Since l > i, a_l ≠ a_i.
            #   So a_l ∉ {b_1..b_{j-1}} iff posB[a_l] >= j.
            #   So new i' = smallest l > i with posB[a_l] >= j.
            # New Bob's pointer: smallest m >= j with b_m ∉ T'.
            #   If j was Bob's pointer before, b_j ∉ T (so posA[b_j] >= i). After T' = T ∪ {a_i}:
            #   b_m ∉ T' iff posA[b_m] >= i AND b_m != a_i.
            #   Hmm but also m > earlier ones (we want smallest).
            #   Actually I realize: Bob's pointer should advance past taken items.
            #   So new j' = smallest m >= j with b_m ∉ T'.
            #   b_j ∉ T' iff b_j ≠ a_i iff posB[a_i] ≠ j iff c_i ≠ j.
            #   If c_i > j: new j' = j (b_j still not taken).
            #   If c_i = j: b_j = a_i, taken, so new j' = next m > j with b_m ∉ T'.
            
            # ...
        
        # similarly for Bob.
