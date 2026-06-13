import sys
from collections import deque
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    edges = []
    for _ in range(n-1):
        u, v = map(int, input().split())
        edges.append((u, v))
    
    initial = frozenset(tuple(sorted(e)) for e in edges)
    
    def get_adj(tree_edges):
        adj = [[] for _ in range(n+1)]
        for u, v in tree_edges:
            adj[u].append(v)
            adj[v].append(u)
        return adj
    
    def compute_parent_and_subtree(tree_edges):
        adj = get_adj(tree_edges)
        parent = [0] * (n+1)
        order = []
        visited = [False] * (n+1)
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
        subtree = [1] * (n+1)
        for u in reversed(order):
            if parent[u] != 0:
                subtree[parent[u]] += subtree[u]
        return parent, subtree, adj
    
    def is_conquered(parent, subtree):
        whites = [v for v in range(1, n+1) if subtree[v] % 2 == 0]
        if not whites:
            return True
        depth = {}
        for w in whites:
            d = 0
            cur = w
            while cur != 0:
                d += 1
                cur = parent[cur]
            depth[w] = d
        deepest = max(whites, key=lambda x: depth[x])
        path = set()
        cur = deepest
        while cur != 0:
            path.add(cur)
            cur = parent[cur]
        return all(w in path for w in whites)
    
    visited = {initial}
    queue = deque([initial])
    conquered_count = 0
    
    while queue:
        tree = queue.popleft()
        parent, subtree, adj = compute_parent_and_subtree(tree)
        
        if is_conquered(parent, subtree):
            conquered_count += 1
        
        for w in range(2, n+1):
            if subtree[w] % 2 == 0:
                pw = parent[w]
                removed_edge = tuple(sorted((pw, w)))
                remaining = tree - {removed_edge}
                
                adj2 = [[] for _ in range(n+1)]
                for u, v in remaining:
                    adj2[u].append(v)
                    adj2[v].append(u)
                
                comp1 = set()
                stack = [1]
                comp1.add(1)
                while stack:
                    u = stack.pop()
                    for v in adj2[u]:
                        if v not in comp1:
                            comp1.add(v)
                            stack.append(v)
                
                compw = set(range(1, n+1)) - comp1
                
                for a in comp1:
                    for b in compw:
                        new_edge = tuple(sorted((a, b)))
                        new_tree = remaining | {new_edge}
                        if new_tree not in visited:
                            visited.add(new_tree)
                            queue.append(new_tree)
    
    print(conquered_count % MOD)

t = int(input())
for _ in range(t):
    solve()
