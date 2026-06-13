import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        v = [int(input_data[idx+i]) for i in range(n)]; idx += n
        a = [int(input_data[idx+i]) for i in range(n)]; idx += n
        b = [int(input_data[idx+i]) for i in range(n)]; idx += n
        
        # Compute β_k for k=1..n (1-indexed)
        # item at α-position k is a[k-1]. β(item) = position in b.
        pos_b = [0] * (n+1)
        for i, x in enumerate(b):
            pos_b[x] = i + 1  # 1-indexed
        
        beta = [0] * (n+1)  # beta[k] = β rank of item at α-position k (1-indexed)
        w = [0] * (n+1)
        for k in range(1, n+1):
            item = a[k-1]
            beta[k] = pos_b[item]
            w[k] = v[item - 1]
        
        # Segment tree over M ∈ {0, 1, ..., n} (size n+1).
        # Operations: range add, prefix max query, point assignment (or max-update).
        # Initial: dp[0] = 0, rest = -inf.
        
        NEG_INF = -10**18
        size = 1
        while size < n + 1:
            size *= 2
        tree = [NEG_INF] * (2 * size)
        lazy = [0] * (2 * size)
        
        # Build initial: dp[0] = 0.
        tree[size + 0] = 0
        for i in range(size - 1, 0, -1):
            tree[i] = max(tree[2*i], tree[2*i+1])
        
        def push(node):
            if lazy[node] != 0:
                for child in (2*node, 2*node+1):
                    tree[child] += lazy[node]
                    lazy[child] += lazy[node]
                lazy[node] = 0
        
        def update_range(node, node_l, node_r, l, r, val):
            if r < node_l or node_r < l:
                return
            if l <= node_l and node_r <= r:
                tree[node] += val
                lazy[node] += val
                return
            push(node)
            mid = (node_l + node_r) // 2
            update_range(2*node, node_l, mid, l, r, val)
            update_range(2*node+1, mid+1, node_r, l, r, val)
            tree[node] = max(tree[2*node], tree[2*node+1])
        
        def query_range(node, node_l, node_r, l, r):
            if r < node_l or node_r < l:
                return NEG_INF
            if l <= node_l and node_r <= r:
                return tree[node]
            push(node)
            mid = (node_l + node_r) // 2
            return max(query_range(2*node, node_l, mid, l, r),
                       query_range(2*node+1, mid+1, node_r, l, r))
        
        def point_set(node, node_l, node_r, pos, val):
            if node_l == node_r:
                tree[node] = val
                return
            push(node)
            mid = (node_l + node_r) // 2
            if pos <= mid:
                point_set(2*node, node_l, mid, pos, val)
            else:
                point_set(2*node+1, mid+1, node_r, pos, val)
            tree[node] = max(tree[2*node], tree[2*node+1])
        
        for k in range(1, n+1):
            β = beta[k]
            wk = w[k]
            # 1. Prefix max [0, β].
            prefix_max = query_range(1, 0, size-1, 0, β)
            # 2. Range add w to [0, β-1].
            if β >= 1:
                update_range(1, 0, size-1, 0, β-1, wk)
            # 3. Point set dp[β] = prefix_max.
            # But after range add to [0, β-1], dp[β] is unchanged. Set it to prefix_max if larger.
            current_β = query_range(1, 0, size-1, β, β)
            new_β = max(current_β, prefix_max)
            point_set(1, 0, size-1, β, new_β)
        
        ans = query_range(1, 0, size-1, 0, n)
        out.append(str(ans))
    
    print('\n'.join(out))

solve()
