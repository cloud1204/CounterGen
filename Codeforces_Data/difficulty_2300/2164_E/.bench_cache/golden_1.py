import sys
from itertools import permutations, product

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    T = int(input_data[idx]); idx+=1
    out = []
    for _ in range(T):
        n, m = int(input_data[idx]), int(input_data[idx+1]); idx+=2
        edges = []
        for i in range(m):
            u,v,w = int(input_data[idx]), int(input_data[idx+1]), int(input_data[idx+2])
            idx+=3
            edges.append((u,v,w))
        # compute f(x,z) for all pairs
        parent = list(range(n+1))
        def find(a):
            while parent[a]!=a:
                parent[a]=parent[parent[a]]
                a=parent[a]
            return a
        # f[x][z]
        INF = float('inf')
        f = [[0 if x==z else INF for z in range(n+1)] for x in range(n+1)]
        # process edges in order, when union happens, all pairs across components get w_i
        # brute: after each edge i (1-indexed), for all pairs in same component, if f still INF set to w_i
        for i,(u,v,w) in enumerate(edges):
            ru,rv = find(u), find(v)
            if ru!=rv:
                parent[ru]=rv
            # update pairs
            comp = {}
            for x in range(1,n+1):
                r = find(x)
                comp.setdefault(r,[]).append(x)
            for r,verts in comp.items():
                for a in verts:
                    for b in verts:
                        if f[a][b]==INF:
                            f[a][b]=w
        
        if m==0:
            out.append('0')
            continue
        
        best = INF
        # try all permutations and directions
        for perm in permutations(range(m)):
            for dirs in product([0,1], repeat=m):
                cost = 0
                cur = 1
                for k,ei in enumerate(perm):
                    u,v,w = edges[ei]
                    if dirs[k]==0:
                        a,b = u,v
                    else:
                        a,b = v,u
                    # transfer from cur to a
                    if cur != a:
                        if f[cur][a]==INF:
                            cost = INF; break
                        cost += f[cur][a]
                    cost += w
                    cur = b
                    if cost>=best: break
                if cost<INF and cur!=1:
                    if f[cur][1]==INF:
                        continue
                    cost += f[cur][1]
                if cost<best:
                    best=cost
        out.append(str(best))
    print('\n'.join(out))

solve()
