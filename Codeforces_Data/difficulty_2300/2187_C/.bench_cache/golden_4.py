import sys
from sys import stdin

def solve():
    input_data = stdin.read().split()
    idx = 0
    t_cases = int(input_data[idx]); idx+=1
    results = []
    for _ in range(t_cases):
        n, m = int(input_data[idx]), int(input_data[idx+1]); idx+=2
        out = [[] for _ in range(n+1)]
        for i in range(1, n):
            out[i].append(i+1)
        for _ in range(m):
            u, v = int(input_data[idx]), int(input_data[idx+1]); idx+=2
            out[u].append(v)
        
        INF = float('inf')
        # V[j][t]: None = Jerry wins, else int
        V = [[None]*(n+1) for _ in range(n+1)]
        
        for j in range(n-1, 0, -1):
            for t in range(1, n+1):
                if j == t: continue
                # Jerry's choices
                jerry_options = out[j]
                # For each j', compute Tom's best response
                best_for_jerry = None  # we'll track
                jerry_wins_possible = False
                max_tom_moves = -1
                for jp in jerry_options:
                    # Tom's options
                    tom_options = [t] + out[t]
                    best_tom = None  # None means Jerry wins inevitably; else min moves
                    for tp in tom_options:
                        move_cost = 1 if tp != t else 0
                        if jp == tp:
                            # Tom wins this turn
                            cand = move_cost
                        elif jp == n:
                            cand = None  # Jerry wins
                        else:
                            sub = V[jp][tp]
                            if sub is None:
                                cand = None
                            else:
                                cand = sub + move_cost
                        if cand is not None:
                            if best_tom is None or cand < best_tom:
                                best_tom = cand
                    # best_tom is None means all Tom's options lead to Jerry win
                    if best_tom is None:
                        jerry_wins_possible = True
                    else:
                        if best_tom > max_tom_moves:
                            max_tom_moves = best_tom
                
                if jerry_wins_possible:
                    V[j][t] = None
                else:
                    V[j][t] = max_tom_moves
        
        total = 0
        for x in range(1, n+1):
            for y in range(1, n+1):
                if x == y: continue
                if x == n:
                    continue
                v = V[x][y]
                if v is not None:
                    total += v
        results.append(total)
    print('\n'.join(map(str, results)))

solve()
