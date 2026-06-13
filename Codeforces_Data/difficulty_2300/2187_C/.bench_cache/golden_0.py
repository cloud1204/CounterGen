import sys
from sys import setrecursionlimit

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        m = int(input_data[idx]); idx += 1
        adj = [[] for _ in range(n+1)]
        for i in range(1, n):
            adj[i].append(i+1)
        for _ in range(m):
            u = int(input_data[idx]); idx += 1
            v = int(input_data[idx]); idx += 1
            adj[u].append(v)
        
        memo = {}
        
        def f(x, y):
            if x == n:
                return -1
            if (x,y) in memo:
                return memo[(x,y)]
            memo[(x,y)] = -1  # to prevent infinite... but graph is DAG so shouldn't cycle
            
            jerry_results = []
            jerry_wins = False
            for xp in adj[x]:
                if xp == y:
                    jerry_results.append(0)
                    continue
                tom_options = []
                if xp != n:
                    sub = f(xp, y)
                    if sub != -1:
                        tom_options.append(sub)
                for yp in adj[y]:
                    if yp == xp:
                        tom_options.append(1)
                    elif xp != n:
                        sub = f(xp, yp)
                        if sub != -1:
                            tom_options.append(sub + 1)
                if tom_options:
                    jerry_results.append(min(tom_options))
                else:
                    jerry_wins = True
                    break
            if jerry_wins:
                memo[(x,y)] = -1
                return -1
            res = max(jerry_results) if jerry_results else -1
            memo[(x,y)] = res
            return res
        
        total = 0
        for x in range(1, n+1):
            for y in range(1, n+1):
                if x != y:
                    r = f(x, y)
                    if r > 0:
                        total += r
        results.append(total)
    
    print('\n'.join(map(str, results)))

solve()
