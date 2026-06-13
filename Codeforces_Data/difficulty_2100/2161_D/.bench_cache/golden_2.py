import sys
from bisect import bisect_right

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        a = [int(x) for x in input_data[idx:idx+n]]; idx+=n
        pos = [[] for _ in range(n+2)]
        for i,x in enumerate(a, start=1):
            pos[x].append(i)
        last = [-1]*(n+2)
        for v in range(1, n+1):
            if pos[v]:
                last[v] = pos[v][-1]
        best_g = 0
        g_inf = 0
        for v in range(n, 0, -1):
            new_best_g_next = best_g
            new_g_inf_next = g_inf
            if not pos[v]:
                new_best = best_g
                new_inf = best_g
            else:
                k = len(pos[v])
                lv1 = last[v+1] if v+1 <= n else -1
                p1 = pos[v][0]
                if p1 > lv1:
                    A = k + best_g
                else:
                    A = k + g_inf
                i = bisect_right(pos[v], lv1)
                if i < k:
                    own_B = k - i
                    B = own_B + best_g
                else:
                    B = -1
                C = best_g
                new_best = max(A, B, C)
                new_inf = best_g
            best_g = new_best
            g_inf = new_inf
        out.append(str(n - best_g))
    print('\n'.join(out))

solve()
