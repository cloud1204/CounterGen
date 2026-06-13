import heapq

def solve():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u-1, v-1, w))
    
    if m == 0:
        print(0)
        return
    
    # Compute j_0(x,z) for all pairs via Kruskal by index
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    # j_0[x][z] = smallest j s.t. edges 1..j connect x,z
    j0 = [[float('inf')]*n for _ in range(n)]
    for i in range(n): j0[i][i] = 0
    
    parent = list(range(n))
    comp_members = [[i] for i in range(n)]
    
    for i, (u,v,w) in enumerate(edges, 1):
        ru, rv = find(u), find(v)
        if ru != rv:
            # merge: all pairs (a in comp[ru], b in comp[rv]) get j_0 = i
            # ... but we need to track members
            if len(comp_members[ru]) < len(comp_members[rv]):
                ru, rv = rv, ru
            for a in comp_members[ru]:
                for b in comp_members[rv]:
                    j0[a][b] = i
                    j0[b][a] = i
            comp_members[ru].extend(comp_members[rv])
            comp_members[rv] = []
            parent[rv] = ru
    
    # suffix_min over edges
    suf = [0]*(m+2)
    suf[m+1] = float('inf')
    for i in range(m, 0, -1):
        suf[i] = min(suf[i+1], edges[i-1][2])
    
    # transfer cost f(x,z)
    def f(x,z):
        if x == z: return 0
        j = j0[x][z]
        if j == float('inf'): return float('inf')
        return suf[j]
    
    # Dijkstra
    full = (1 << m) - 1
    INF = float('inf')
    dist = {}
    start = (0, 0)  # at vertex 0 (1-indexed 1), no edges marked
    dist[start] = 0
    pq = [(0, 0, 0)]
    
    while pq:
        d, v, S = heapq.heappop(pq)
        if d > dist.get((v,S), INF): continue
        if v == 0 and S == full:
            print(d)
            return
        # transitions
        # mark each edge
        for i, (u, vv, w) in enumerate(edges):
            if u == v:
                nv = vv
            elif vv == v:
                nv = u
            else:
                continue
            nS = S | (1 << i)
            nd = d + w
            if nd < dist.get((nv, nS), INF):
                dist[(nv, nS)] = nd
                heapq.heappush(pq, (nd, nv, nS))
        # transfer
        for z in range(n):
            if z == v: continue
            c = f(v, z)
            if c == INF: continue
            nd = d + c
            if nd < dist.get((z, S), INF):
                dist[(z, S)] = nd
                heapq.heappush(pq, (nd, z, S))

T = int(input())
for _ in range(T):
    solve()
