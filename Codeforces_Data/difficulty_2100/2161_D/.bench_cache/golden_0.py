import sys
from collections import defaultdict
from bisect import bisect_left

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        maxv = max(a) if a else 0
        # positions[v] = sorted list of positions (1-indexed) of value v in a
        positions = defaultdict(list)
        for i, x in enumerate(a):
            positions[x].append(i + 1)
        
        # state[l] = (limit, chain_total) for chain starting at l, processed up to current v
        # We'll maintain as v increases.
        INF = n + 1
        # Initialize for each l, chain state is "not started yet" until v reaches l.
        # Easier: state[l] is initialized when v == l.
        
        limit = [0] * (maxv + 2)  # limit[l] = current limit for chain l
        ctotal = [0] * (maxv + 2)  # chain total for chain l
        alive = [False] * (maxv + 2)  # whether chain l is started
        
        dp = [0] * (maxv + 2)
        # de[v] = ... we'll compute inline
        dp_prev2 = 0  # dp[-1]
        dp_prev1 = 0  # dp[0]
        # We'll need dp[v-2], dp[v-1] etc., so store dp array.
        dp[0] = 0
        # dp[-1] convention: use dp[0]=0 as well; treat l-2 < 0 as 0.
        
        for v in range(1, maxv + 1):
            # For each l from 1 to v, update chain(l, v) and de[v].
            de_v = 0
            # Start chain l = v
            limit[v] = INF
            ctotal[v] = 0
            alive[v] = True
            
            for l in range(1, v + 1):
                # Process value v in chain l.
                # count of v in [1, limit[l] - 1]
                lst = positions[v]
                # number of positions ≤ limit[l] - 1
                cnt = bisect_left(lst, limit[l])
                ctotal[l] += cnt
                if cnt > 0:
                    limit[l] = lst[0]  # first occurrence in valid range
                    # Wait, first occurrence of v in [1, limit[l]-1] is lst[0] if lst[0] < limit[l].
                    # Actually lst is sorted, so first occurrence in [1, limit[l]-1] is lst[0] if lst[0] < limit[l].
                    limit[l] = lst[0]
                else:
                    limit[l] = INF  # reset
                
                # Update de_v
                dp_lm2 = dp[l - 2] if l >= 2 else 0
                de_v = max(de_v, dp_lm2 + ctotal[l])
            
            dp[v] = max(dp[v - 1], de_v)
        
        out.append(str(n - dp[maxv]))
    
    print('\n'.join(out))

solve()
