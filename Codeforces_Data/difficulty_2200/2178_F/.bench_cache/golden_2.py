import sys
from sys import stdin

MOD = 998244353

def solve():
    input_data = stdin.read().split()
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
        ans = brute_force(n, edges)
        results.append(ans)
    print('\n'.join(map(str, results)))

def get_parent_subtree(n, adj):
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
    subsize = [1]*(n+1)
    for u in reversed(order):
        if parent[u] != 0:
            subsize[parent[u]] += subsize[u]
    return parent, subsize, order

def is_conquered(n, edges_tuple):
    adj = [[] for _ in range(n+1)]
    for u,v in edges_tuple:
        adj[u].append(v)
        adj[v].append(u)
    parent, subsize, order = get_parent_subtree(n, adj)
    whites = [v for v in range(1, n+1) if subsize[v] % 2 == 0]
    if not whites:
        return True
    # check if whites form a chain from root
    # sort whites by depth (= subtree size? no, by subsize they're not ordered well)
    # actually let's find ancestry
    # build depth
    depth = [0]*(n+1)
    for u in order:
        if parent[u] != 0:
            depth[u] = depth[parent[u]] + 1
    whites.sort(key=lambda x: depth[x])
    # check chain
    for i in range(1, len(whites)):
        # whites[i] should be descendant of whites[i-1]
        v = whites[i]
        target = whites[i-1]
        while v != 0 and v != target:
            v = parent[v]
        if v != target:
            return False
    return True

def brute_force(n, edges):
    start = frozenset(tuple(sorted(e)) for e in edges)
    visited = {start}
    queue = [start]
    count = 0
    while queue:
        cur = queue.pop()
        edges_list = list(cur)
        adj = [[] for _ in range(n+1)]
        for u,v in edges_list:
            adj[u].append(v)
            adj[v].append(u)
        parent, subsize, order = get_parent_subtree(n, adj)
        if is_conquered_from_state(n, parent, subsize):
            count += 1
        # try all operations
        whites = [v for v in range(2, n+1) if subsize[v] % 2 == 0]
        for w in whites:
            # remove edge (parent[w], w), get two components
            # w-component: subtree of w
            w_comp = set()
            stack = [w]
            while stack:
                x = stack.pop()
                w_comp.add(x)
                for y in adj[x]:
                    if y != parent[x] and y not in w_comp:
                        # need to traverse subtree
                        pass
            # easier: w_comp = descendants of w including w
            w_comp = set()
            stack = [w]
            while stack:
                x = stack.pop()
                w_comp.add(x)
                for y in adj[x]:
                    if y in w_comp: continue
                    if y == parent[x]: continue
                    w_comp.add(y)
                    stack.append(y)
            other = set(range(1, n+1)) - w_comp
            # remove edge (parent[w], w)
            base_edges = set(cur) - {tuple(sorted((parent[w], w)))}
            # try all u in w_comp, r in other
            for u in w_comp:
                for r in other:
                    new_edge = tuple(sorted((u, r)))
                    new_edges = base_edges | {new_edge}
                    fs = frozenset(new_edges)
                    if fs not in visited:
                        visited.add(fs)
                        queue.append(fs)
    return count % MOD

def is_conquered_from_state(n, parent, subsize):
    whites = [v for v in range(1, n+1) if subsize[v] % 2 == 0]
    if not whites:
        return True
    depth = {}
    depth[1] = 0
    # compute depths via parent
    def get_depth(v):
        d = 0
        while parent[v] != 0:
            d += 1
            v = parent[v]
        return d
    for v in whites:
        depth[v] = get_depth(v)
    whites.sort(key=lambda x: depth[x])
    for i in range(1, len(whites)):
        v = whites[i]
        target = whites[i-1]
        while v != 0 and v != target:
            v = parent[v]
        if v != target:
            return False
    return True

solve()
