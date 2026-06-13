import sys
from sys import stdin

def solve():
    input_data = stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        v = [int(x) for x in input_data[idx:idx+n]]; idx += n
        a = [int(x) for x in input_data[idx:idx+n]]; idx += n
        b = [int(x) for x in input_data[idx:idx+n]]; idx += n
        pos_b = [0] * (n + 1)
        for i, x in enumerate(b):
            pos_b[x] = i
        u = [v[a[i] - 1] for i in range(n)]
        f = [pos_b[a[i]] for i in range(n)]
        
        # Segment tree with range add, range max, point max-update.
        size = n + 1  # indices 0..n
        N = 1
        while N < size:
            N *= 2
        NEG_INF = float('-inf')
        tree = [NEG_INF] * (2 * N)
        lazy = [0] * (2 * N)
        tree[N + 0] = 0  # dp[0] = 0
        for i in range(N - 1, 0, -1):
            tree[i] = max(tree[2*i], tree[2*i+1])
        
        def push(node):
            if lazy[node]:
                for c in (2*node, 2*node+1):
                    tree[c] += lazy[node]
                    lazy[c] += lazy[node]
                lazy[node] = 0
        
        def update_add(node, node_l, node_r, l, r, val):
            if r < node_l or node_r < l:
                return
            if l <= node_l and node_r <= r:
                tree[node] += val
                lazy[node] += val
                return
            push(node)
            mid = (node_l + node_r) // 2
            update_add(2*node, node_l, mid, l, r, val)
            update_add(2*node+1, mid+1, node_r, l, r, val)
            tree[node] = max(tree[2*node], tree[2*node+1])
        
        def query_max(node, node_l, node_r, l, r):
            if r < node_l or node_r < l:
                return NEG_INF
            if l <= node_l and node_r <= r:
                return tree[node]
            push(node)
            mid = (node_l + node_r) // 2
            return max(query_max(2*node, node_l, mid, l, r),
                       query_max(2*node+1, mid+1, node_r, l, r))
        
        def point_max_update(node, node_l, node_r, p, val):
            if node_l == node_r:
                tree[node] = max(tree[node], val)
                return
            push(node)
            mid = (node_l + node_r) // 2
            if p <= mid:
                point_max_update(2*node, node_l, mid, p, val)
            else:
                point_max_update(2*node+1, mid+1, node_r, p, val)
            tree[node] = max(tree[2*node], tree[2*node+1])
        
        for i in range(n):
            c = f[i]
            ui = u[i]
            val = query_max(1, 0, N-1, 0, c+1)
            if c >= 0:
                update_add(1, 0, N-1, 0, c, ui)
            point_max_update(1, 0, N-1, c+1, val)
        
        ans = query_max(1, 0, N-1, 0, n)
        results.append(ans)
    
    print('\n'.join(map(str, results)))

solve()
