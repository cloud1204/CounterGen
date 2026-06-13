import sys
from sys import setrecursionlimit
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = [x % 2 for x in a]
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    
    if n == 1:
        if b[0] == 1:
            print("YES")
            print(1)
        else:
            print("NO")
        return
    
    root = 0
    parent = [-1] * n
    order = []
    # BFS to get order and parents
    from collections import deque
    visited = [False] * n
    visited[root] = True
    dq = deque([root])
    while dq:
        u = dq.popleft()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                dq.append(v)
    
    children = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != -1:
            children[parent[v]].append(v)
    
    # dp[v] = set of feasible w_v values (subset of {0,1})
    # Also need to record combined children achievable set for each v (for reconstruction)
    dp = [set() for _ in range(n)]
    # children_set[v] = set of achievable T values from combining children (each child picks a valid w_c)
    children_set = [set() for _ in range(n)]
    
    # Process in reverse order
    for v in reversed(order):
        # Compute children_set[v]
        cur = {0}
        feasible = True
        for c in children[v]:
            f_c = set()
            for wc in dp[c]:
                f_c.add((wc * b[c]) % 2)
            if not f_c:
                feasible = False
                break
            new_cur = set()
            for x in cur:
                for y in f_c:
                    new_cur.add((x + y) % 2)
            cur = new_cur
        if not feasible:
            children_set[v] = set()
        else:
            children_set[v] = cur
        
        if parent[v] == -1:
            # root: need b_v + T ≡ 1, T ≡ 1 + b_v
            target = (1 + b[v]) % 2
            if target in children_set[v]:
                dp[v] = {0}  # placeholder, root has no w
            else:
                dp[v] = set()
        else:
            bp = b[parent[v]]
            for wv in [0, 1]:
                xv = 1 - wv
                target = (1 + b[v] + xv * bp) % 2
                if target in children_set[v]:
                    dp[v].add(wv)
    
    if not dp[root]:
        print("NO")
        return
    
    # Reconstruct
    w = [0] * n  # w_v for non-root; for root unused
    # For root, determine which assignment of children's w_c gives target
    # Then propagate
    
    # We process in BFS order (top-down)
    # For each v, given w[v] (or for root), determine target T for children and assign w_c
    
    target_v = [0] * n  # T value needed for v's children combined
    if parent[root] == -1:
        target_v[root] = (1 + b[root]) % 2
    
    # Process in order (top-down)
    for v in order:
        if parent[v] != -1:
            xv = 1 - w[v]
            bp = b[parent[v]]
            target_v[v] = (1 + b[v] + xv * bp) % 2
        # Now assign w[c] for each child c
        T = target_v[v]
        # We need sum_c (w[c] * b[c]) ≡ T mod 2, with each w[c] ∈ dp[c]
        # Greedy: for each child, try to find feasible assignment
        # We need to do this such that we can reach T. We have feasibility from DP.
        # Process children one by one. Track current sum parity.
        # For each child, choices: w[c] ∈ dp[c], contribution = w[c] * b[c] mod 2.
        # We want final parity = T.
        # Need to do a feasibility check as we go.
        # Precompute suffix achievable sets.
        
        cs = children[v]
        k = len(cs)
        # contribution sets
        contrib = []
        for c in cs:
            s = set()
            mp = {}  # contribution -> w[c] choice
            for wc in dp[c]:
                ct = (wc * b[c]) % 2
                if ct not in mp:
                    mp[ct] = wc
                s.add(ct)
            contrib.append((s, mp))
        # suffix achievable: suffix[i] = set of achievable sums from children i..k-1
        suffix = [set() for _ in range(k+1)]
        suffix[k] = {0}
        for i in range(k-1, -1, -1):
            s, _ = contrib[i]
            new_s = set()
            for x in s:
                for y in suffix[i+1]:
                    new_s.add((x+y) % 2)
            suffix[i] = new_s
        
        cur_sum = 0
        for i, c in enumerate(cs):
            s, mp = contrib[i]
            # Need to choose ct ∈ s such that (T - cur_sum - ct) mod 2 is in suffix[i+1]
            chosen = None
            for ct in s:
                needed = (T - cur_sum - ct) % 2
                if needed in suffix[i+1]:
                    chosen = ct
                    break
            assert chosen is not None
            w[c] = mp[chosen]
            cur_sum = (cur_sum + chosen) % 2
    
    # Now we have w[v] for non-root v. x[v] = 1 - w[v].
    # For each non-root v: if x[v]=1, v removed before parent; else after.
    # Build DAG and topo sort.
    
    in_deg = [0] * n
    graph = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != -1:
            p = parent[v]
            xv = 1 - w[v]
            if xv == 1:
                # v before p
                graph[v].append(p)
                in_deg[p] += 1
            else:
                graph[p].append(v)
                in_deg[v] += 1
    
    dq = deque()
    for i in range(n):
        if in_deg[i] == 0:
            dq.append(i)
    result = []
    while dq:
        u = dq.popleft()
        result.append(u + 1)
        for v in graph[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                dq.append(v)
    
    print("YES")
    print(*result)

t = int(input())
for _ in range(t):
    solve()
