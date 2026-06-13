import sys
from sys import stdin
input = stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    edges = []
    for _ in range(n-1):
        u, v = map(int, input().split())
        edges.append((u,v))
    
    def tree_key(edge_set):
        return tuple(sorted((min(u,v), max(u,v)) for u,v in edge_set))
    
    def compute_coloring(edge_set, n):
        adj = [[] for _ in range(n+1)]
        for u,v in edge_set:
            adj[u].append(v)
            adj[v].append(u)
        parent = [0]*(n+1)
        order = []
        visited = [False]*(n+1)
        stack = [1]
        visited[1] = True
        parent[1] = 0
        while stack:
            u = stack.pop()
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    stack.append(v)
        size = [1]*(n+1)
        for u in reversed(order):
            if parent[u] != 0:
                size[parent[u]] += size[u]
        white = [size[v] % 2 == 0 for v in range(n+1)]
        return white, parent, adj
    
    def is_conquered(white, parent, n):
        whites = [v for v in range(1,n+1) if white[v]]
        if not whites:
            return True
        ancestors = {}
        for w in whites:
            anc = set()
            cur = w
            while cur != 0:
                anc.add(cur)
                cur = parent[cur]
            ancestors[w] = anc
        whites_sorted = sorted(whites, key=lambda w: len(ancestors[w]), reverse=True)
        deepest = whites_sorted[0]
        path_to_deepest = ancestors[deepest]
        for w in whites:
            if w not in path_to_deepest:
                return False
        return True
    
    initial = frozenset((min(u,v),max(u,v)) for u,v in edges)
    visited = {initial}
    queue = [initial]
    conquered_count = 0
    
    while queue:
        new_queue = []
        for state in queue:
            edge_list = list(state)
            white, parent, adj = compute_coloring(edge_list, n)
            if is_conquered(white, parent, n):
                conquered_count += 1
            for v in range(2, n+1):
                if white[v]:
                    pw = parent[v]
                    remaining = state - {(min(pw,v),max(pw,v))}
                    adj2 = [[] for _ in range(n+1)]
                    for a,b in remaining:
                        adj2[a].append(b)
                        adj2[b].append(a)
                    comp_v = set()
                    st = [v]
                    comp_v.add(v)
                    while st:
                        x = st.pop()
                        for y in adj2[x]:
                            if y not in comp_v:
                                comp_v.add(y)
                                st.append(y)
                    comp_root = set(range(1,n+1)) - comp_v
                    for a in comp_root:
                        for b in comp_v:
                            new_edge = (min(a,b), max(a,b))
                            new_state = remaining | {new_edge}
                            if new_state not in visited:
                                visited.add(new_state)
                                new_queue.append(new_state)
        queue = new_queue
    
    print(conquered_count % MOD)

t = int(input())
for _ in range(t):
    solve()
