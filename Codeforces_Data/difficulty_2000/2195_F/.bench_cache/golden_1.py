import sys
from sys import setrecursionlimit

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        funcs = []
        for i in range(n):
            a = int(input_data[idx]); idx += 1
            b = int(input_data[idx]); idx += 1
            c = int(input_data[idx]); idx += 1
            funcs.append((a, b, c))
        
        # dom[i][j] = True if i dominates j (i(x) > j(x) for all x)
        # build adjacency: edges from j to i if i dominates j (so chains go up)
        # children[i] = list of j that i dominates (i > j)
        # parents[i] = list of j that dominate i
        
        children = [[] for _ in range(n)]
        parents = [[] for _ in range(n)]
        
        for i in range(n):
            ai, bi, ci = funcs[i]
            for j in range(i+1, n):
                aj, bj, cj = funcs[j]
                da = ai - aj
                db = bi - bj
                dc = ci - cj
                if da == 0:
                    if db == 0:
                        # dc != 0
                        if dc > 0:
                            children[i].append(j)
                            parents[j].append(i)
                        else:
                            children[j].append(i)
                            parents[i].append(j)
                    # else dependent
                else:
                    # discriminant db^2 - 4*da*dc < 0?
                    disc = db*db - 4*da*dc
                    if disc < 0:
                        # f_i - f_j has no real root, sign determined by da
                        if da > 0:
                            # i - j > 0 everywhere -> i dominates j
                            children[i].append(j)
                            parents[j].append(i)
                        else:
                            children[j].append(i)
                            parents[i].append(j)
        
        down = [0]*n
        up = [0]*n
        
        # compute down via DFS with memo
        def compute_down(i):
            if down[i] != 0: return down[i]
            best = 1
            for j in children[i]:
                v = compute_down(j) + 1
                if v > best: best = v
            down[i] = best
            return best
        
        def compute_up(i):
            if up[i] != 0: return up[i]
            best = 1
            for j in parents[i]:
                v = compute_up(j) + 1
                if v > best: best = v
            up[i] = best
            return best
        
        for i in range(n):
            compute_down(i)
            compute_up(i)
        
        res = [str(down[i] + up[i] - 1) for i in range(n)]
        out.append(' '.join(res))
    
    print('\n'.join(out))

solve()
