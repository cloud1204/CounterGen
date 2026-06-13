import sys
from bisect import bisect_right, bisect_left

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        # Group positions by value
        from collections import defaultdict
        P = defaultdict(list)
        for i, v in enumerate(a):
            P[v].append(i+1)  # 1-indexed positions
        maxV = max(a)
        # dp[v] is dict or list of (M, value)
        # We track states as list of (M, dp_value), sorted by M.
        # Initial: v = maxV+1, states = [(0, 0)]
        states = [(0, 0)]  # list of (M', dp_value), sorted by M'.
        for v in range(maxV, 0, -1):
            Pv = P[v]
            nv = len(Pv)
            if nv == 0:
                # Only M=0 state. dp[v][0] = max over states.
                best = max(s[1] for s in states)
                states = [(0, best)]
                continue
            # Compute g(M') = dp_value - f(M') where f(M') = # Pv ≤ M'
            # Sort states by M' (already sorted).
            # For each M' in states, f(M') = bisect_right(Pv, M').
            g_list = []  # (M', g_value)
            for M_prev, dpv in states:
                f_Mprev = bisect_right(Pv, M_prev)
                g_list.append((M_prev, dpv - f_Mprev))
            # Now compute new states for v.
            # For M ∈ Pv: dp[v][M] = f(M) + max g over M'<M.
            # f(M) for M ∈ Pv is index in Pv (1-indexed).
            # Maintain running max of g as we go through M_prev sorted.
            # Iterate through Pv (sorted) and through g_list (sorted by M_prev). Merge.
            new_states = []
            # First, dp[v][0] = max over all M' of dp_value
            best_overall = max(s[1] for s in states)
            new_states.append((0, best_overall))
            # For M ∈ Pv: dp[v][M] = (index+1) + max g(M') for M' < M.
            j = 0  # pointer into g_list
            running_max_g = -float('inf')
            # We need M' < M strictly. g_list is sorted by M_prev.
            for i_pv, M in enumerate(Pv):
                # Advance j while g_list[j].M_prev < M
                while j < len(g_list) and g_list[j][0] < M:
                    running_max_g = max(running_max_g, g_list[j][1])
                    j += 1
                f_M = i_pv + 1
                if running_max_g > -float('inf'):
                    dp_val = f_M + running_max_g
                    new_states.append((M, dp_val))
                # else: no valid M' < M, can't use this state? But M'=0 is always there.
                # Since g_list contains (0, ...) and M ≥ 1 (positions are ≥1), M' = 0 < M always.
                # So running_max_g should always be set after first iteration.
            states = new_states
        ans = n - max(s[1] for s in states)
        out.append(str(ans))
    print('\n'.join(out))

solve()
