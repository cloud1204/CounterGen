import sys
from sys import setrecursionlimit
from collections import deque

MOD = 998244353

def solve(n, edges):
    if n == 1:
        return 1
    
    def compute_subtree_sizes(adj, n):
        size = [0]*(n+1)
        parent = [0]*(n+1)
        order = []
        visited = [False]*(n+1)
        stack = [1]
        visited[1] = True
        parent[1] = 0
        while stack:
            v = stack.pop()
            order.append(v)
            for u in adj[v]:
                if not visited[u]:
                    visited[u] = True
                    parent[u] = v
                    stack.append(u)
        for v in reversed(order):
            size[v] = 1
            for u in adj[v]:
                if u != parent[v]:
                    size[v] += size[u]
        return size, parent
    
    def adj_from_edges(edges, n):
        adj = [[] for _ in range(n+1)]
        for u,v in edges:
            adj[u].append(v)
            adj[v].append(u)
        return adj
    
    def canonical(edges):
        return tuple(sorted((min(u,v), max(u,v)) for u,v in edges))
    
    def is_conquered(edges, n):
        adj = adj_from_edges(edges, n)
        size, parent = compute_subtree_sizes(adj, n)
        whites = [v for v in range(1, n+1) if size[v] % 2 == 0]
        if not whites:
            return True
        # Check if all whites lie on a path from root to some v
        # Sort whites by depth, then check they form a chain
        depth = [0]*(n+1)
        # compute depth
        from collections import deque
        dq = deque([1])
        visited = [False]*(n+1)
        visited[1] = True
        while dq:
            v = dq.popleft()
            for u in adj[v]:
                if not visited[u]:
                    visited[u] = True
                    depth[u] = depth[v]+1
                    dq.append(u)
        whites.sort(key=lambda x: depth[x])
        # The deepest white is v. All other whites must be ancestors of v.
        v = whites[-1]
        ancestors = set()
        cur = v
        while cur != 0:
            ancestors.add(cur)
            cur = parent[cur]
        for w in whites:
            if w not in ancestors:
                return False
        return True
    
    def get_neighbors(edges, n):
        adj = adj_from_edges(edges, n)
        size, parent = compute_subtree_sizes(adj, n)
        # Find white non-root vertices
        whites = [v for v in range(2, n+1) if size[v] % 2 == 0]
        results = []
        for w in whites:
            # Detach subtree of w. Find vertices in subtree.
            subtree_set = set()
            stack = [w]
            visited = {parent[w]}
            visited.add(w)
            subtree_set.add(w)
            while stack:
                v = stack.pop()
                for u in adj[v]:
                    if u not in visited:
                        visited.add(u)
                        subtree_set.add(u)
                        stack.append(u)
            outside = set(range(1, n+1)) - subtree_set
            # New edge from any a in subtree to any b in outside
            base_edges = [e for e in edges if not (e[0]==parent[w] and e[1]==w) and not (e[0]==w and e[1]==parent[w])]
            for a in subtree_set:
                for b in outside:
                    new_edges = base_edges + [(min(a,b), max(a,b))]
                    results.append(new_edges)
        return results
    
    start = canonical(edges)
    visited = {start}
    queue = deque([list(edges)])
    count = 0
    if is_conquered(edges, n):
        count = 1
    while queue:
        cur = queue.popleft()
        for ne in get_neighbors(cur, n):
            key = canonical(ne)
            if key not in visited:
                visited.add(key)
                if is_conquered(ne, n):
                    count += 1
                queue.append(ne)
    return count % MOD

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        edges = []
        for _ in range(n-1):
            u = int(input_data[idx]); idx+=1
            v = int(input_data[idx]); idx+=1
            edges.append((u,v))
        results.append(str(solve(n, edges)))
    print('\n'.join(results))

main()
