import sys
from functools import lru_cache

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    for _ in range(t):
        n, m = int(input_data[idx]), int(input_data[idx+1]); idx+=2
        adj = [[] for _ in range(n+1)]
        for u in range(1, n):
            adj[u].append(u+1)
        for _ in range(m):
            u, v = int(input_data[idx]), int(input_data[idx+1]); idx+=2
            adj[u].append(v)
        
        sys.setrecursionlimit(10**6)
        memo = {}
        
        def game(x, y):
            if x == n:
                return -1  # Jerry already won
            if (x,y) in memo:
                return memo[(x,y)]
            memo[(x,y)] = None  # detect cycles? Actually no cycles since edges go forward.
            
            # Jerry must move (x<n, has at least edge to x+1)
            jerry_choices = adj[x]
            
            # For Jerry's max strategy
            worst_for_tom = 0  # max over jerry choices of (tom's min moves)
            jerry_can_win = False
            
            for xp in jerry_choices:
                # Tom's choices: stay (y) or move to neighbors
                tom_choices = [(y, 0)] + [(yp, 1) for yp in adj[y]]
                
                best_tom = None
                for yp, cost in tom_choices:
                    if xp == yp:
                        # Tom wins this turn
                        if best_tom is None or cost < best_tom:
                            best_tom = cost
                        continue
                    if xp == n:
                        # Jerry reached n, Tom didn't catch
                        continue
                    # Continue game
                    sub = game(xp, yp)
                    if sub == -1:
                        continue
                    total = cost + sub
                    if best_tom is None or total < best_tom:
                        best_tom = total
                
                if best_tom is None:
                    # Jerry wins via this xp
                    jerry_can_win = True
                    break
                if best_tom > worst_for_tom:
                    worst_for_tom = best_tom
            
            if jerry_can_win:
                memo[(x,y)] = -1
                return -1
            memo[(x,y)] = worst_for_tom
            return worst_for_tom
        
        total = 0
        for x in range(1, n+1):
            for y in range(1, n+1):
                if x == y: continue
                r = game(x, y)
                if r != -1:
                    total += r
        print(total)

solve()
