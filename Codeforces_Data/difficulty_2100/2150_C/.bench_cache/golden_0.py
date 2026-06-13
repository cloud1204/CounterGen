import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        v = [int(input_data[idx+i]) for i in range(n)]; idx+=n
        a = [int(input_data[idx+i]) for i in range(n)]; idx+=n
        b = [int(input_data[idx+i]) for i in range(n)]; idx+=n
        pos_b = [0]*(n+1)
        for i in range(n):
            pos_b[b[i]] = i+1
        b_prime = [pos_b[a[i]] for i in range(n)]
        v_prime = [v[a[i]-1] for i in range(n)]
        # Segment tree on positions 1..n+1, with n+1 being +∞.
        size = n+1
        # Use iterative or recursive segtree
        NEG_INF = float('-inf')
        N = 1
        while N < size:
            N *= 2
        tree = [NEG_INF]*(2*N)
        lazy = [0]*(2*N)
        # Initialize: position size (1-indexed) = +∞ slot, set f(size)=0.
        # Build
        # leaves: tree[N+i-1] for position i (1-indexed)? Let's do 0-indexed leaves: leaf j corresponds to position j+1.
        # Actually let me use position index 1..size mapped to leaves 0..size-1 in tree.
        # Set leaf for position size (i.e., +∞ index = size = n+1) to 0.
        for i in range(size):
            if i == size - 1:
                tree[N+i] = 0
            else:
                tree[N+i] = NEG_INF
        for i in range(N-1, 0, -1):
            tree[i] = max(tree[2*i], tree[2*i+1])
        
        def push_down(node):
            if lazy[node]:
                for child in (2*node, 2*node+1):
                    tree[child] += lazy[node]
                    lazy[child] += lazy[node]
                lazy[node] = 0
        
        def range_add(node, node_l, node_r, l, r, val):
            if r < node_l or node_r < l:
                return
            if l <= node_l and node_r <= r:
                tree[node] += val
                lazy[node] += val
                return
            push_down(node)
            mid = (node_l + node_r)//2
            range_add(2*node, node_l, mid, l, r, val)
            range_add(2*node+1, mid+1, node_r, l, r, val)
            tree[node] = max(tree[2*node], tree[2*node+1])
        
        def range_max(node, node_l, node_r, l, r):
            if r < node_l or node_r < l:
                return NEG_INF
            if l <= node_l and node_r <= r:
                return tree[node]
            push_down(node)
            mid = (node_l + node_r)//2
            return max(range_max(2*node, node_l, mid, l, r), range_max(2*node+1, mid+1, node_r, l, r))
        
        def point_assign(node, node_l, node_r, pos, val):
            if node_l == node_r:
                tree[node] = val
                lazy[node] = 0
                return
            push_down(node)
            mid = (node_l + node_r)//2
            if pos <= mid:
                point_assign(2*node, node_l, mid, pos, val)
            else:
                point_assign(2*node+1, mid+1, node_r, pos, val)
            tree[node] = max(tree[2*node], tree[2*node+1])
        
        # Process i from n down to 1
        for i in range(n-1, -1, -1):
            bp = b_prime[i]  # 1..n
            vp = v_prime[i]
            # Q = max f(m) for m >= bp, positions bp..size (1-indexed) -> leaves bp-1..size-1
            Q = range_max(1, 0, N-1, bp-1, size-1)
            # Range add vp to m < bp, positions 1..bp-1 -> leaves 0..bp-2
            if bp > 1:
                range_add(1, 0, N-1, 0, bp-2, vp)
            # Set f(bp) = Q + vp
            point_assign(1, 0, N-1, bp-1, Q + vp)
        
        ans = range_max(1, 0, N-1, 0, size-1)
        out.append(str(max(ans, 0)))
    sys.stdout.write('\n'.join(out)+'\n')

solve()
