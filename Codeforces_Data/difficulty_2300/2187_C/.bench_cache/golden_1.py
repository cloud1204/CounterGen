import sys
from functools import lru_cache
sys.setrecursionlimit(10**6)

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    INF = float('inf')
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        m = int(input_data[idx]); idx+=1
        out = [[] for _ in range(n+1)]
        for i in range(1, n):
            out[i].append(i+1)
        for _ in range(m):
            u = int(input_data[idx]); idx+=1
            v = int(input_data[idx]); idx+=1
            out[u].append(v)
        
        # memo
        memo = {}
        def val(j, t):
            # j != t, j != n (handled), t can be anything 1..n
            if (j,t) in memo:
                return memo[(j,t)]
            # Jerry moves
            jerry_options = out[j] if out[j] else [j]
            best_jerry = -1
            for jp in jerry_options:
                # Tom chooses t' to minimize
                tom_options = [t] + out[t]
                best_tom = INF
                for tp in tom_options:
                    cost = 0 if tp == t else 1
                    if jp == tp:
                        total = cost
                    elif jp == n:
                        total = INF
                    else:
                        sub = val(jp, tp)
                        if sub == INF:
                            total = INF
                        else:
                            total = cost + sub
                    if total < best_tom:
                        best_tom = total
                if best_tom > best_jerry:
                    best_jerry = best_tom
                if best_jerry == INF:
                    break
            memo[(j,t)] = best_jerry
            return best_jerry
        
        total = 0
        for x in range(1, n+1):
            for y in range(1, n+1):
                if x == y: continue
                if x == n:
                    f = 0
                else:
                    v = val(x, y)
                    f = 0 if v == INF else v
                total += f
        results.append(total)
    print('\n'.join(map(str, results)))

solve()
