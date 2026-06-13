import sys
from collections import deque
from sys import setrecursionlimit

MOD = 998244353

def solve(n, edges):
    if n == 1:
        return 1
    
    initial = frozenset((min(u,v), max(u,v)) for u,v in edges)
    
    def get_children(edge_set):
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
            if parent[u]:
                size[parent[u]] += size[u]
        return parent, size, order
    
    def is_conquered(edge_set):
        parent, size, order = get_children(edge_set)
        whites = [v for v in range(1, n+1) if size[v] % 2 == 0]
        if not whites:
            return True
        depths = {}
        for u in order:
            if u == 1:
                depths[u] = 0
            else:
                depths[u] = depths[parent[u]] + 1
        deepest = max(whites, key=lambda v: depths[v])
        path = set()
        cur = deepest
        while cur:
            path.add(cur)
            cur = parent[cur]
        return all(w in path for w in whites)
    
    visited = {initial}
    queue = deque([initial])
    conquered_count = 0
    
    while queue:
        tree = queue.popleft()
        if is_conquered(tree):
            conquered_count += 1
        
        parent, size, order = get_children(tree)
        whites = [v for v in range(2, n+1) if size[v] % 2 == 0]
        
        for w in whites:
            new_base = tree - {(min(parent[w], w), max(parent[w], w))}
            comp_w = set()
            adj = [[] for _ in range(n+1)]
            for u,v in new_base:
                adj[u].append(v)
                adj[v].append(u)
            stack = [w]
            comp_w.add(w)
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if v not in comp_w:
                        comp_w.add(v)
                        stack.append(v)
            comp_other = set(range(1, n+1)) - comp_w
            
            for a in comp_w:
                for b in comp_other:
                    new_edge = (min(a,b), max(a,b))
                    new_tree = new_base | {new_edge}
                    if new_tree not in visited:
                        visited.add(new_tree)
                        queue.append(new_tree)
    
    return conquered_count % MOD

input_data = sys.stdin.read().split()
idx = 0
t = int(input_data[idx]); idx += 1
results = []
for _ in range(t):
    n = int(input_data[idx]); idx += 1
    edges = []
    for _ in range(n-1):
        u = int(input_data[idx]); idx += 1
        v = int(input_data[idx]); idx += 1
        edges.append((u,v))
    results.append(solve(n, edges))
print('\n'.join(map(str, results)))
