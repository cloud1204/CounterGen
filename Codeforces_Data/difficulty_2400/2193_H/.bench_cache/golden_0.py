import sys
from sys import setrecursionlimit
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = [x & 1 for x in a]
    adj = [[] for _ in range(n+1)]  # 1-indexed
    edges = []
    for _ in range(n-1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
        edges.append((u,v))
    
    if n == 1:
        # single vertex: S=0, need b[0] odd (parity differs from 0)
        if b[0] == 1:
            print("YES")
            print(1)
        else:
            print("NO")
        return
    
    # Root at 1, iterative DFS
    parent = [0]*(n+1)
    order = []
    parent[1] = -1
    stack = [1]
    visited = [False]*(n+1)
    visited[1] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # children list
    children = [[] for _ in range(n+1)]
    for v in range(2, n+1):
        children[parent[v]].append(v)
    
    # DP in reverse order
    dp0 = [False]*(n+1)
    dp1 = [False]*(n+1)
    # for reconstruction, we'll choose during top-down pass
    
    for u in reversed(order):
        bp = b[parent[u]-1] if parent[u] != -1 else 0
        # For e in {0, 1} (if root only e=0 matters)
        for e in (0, 1):
            if parent[u] == -1 and e == 1:
                continue
            # check children
            forced_sum = 0
            free_count = 0
            ok = True
            for c in children[u]:
                ok0 = dp0[c]
                ok1 = dp1[c]
                # e(c) = 1 - f_c, where f_c is what we choose
                # dp(c, e(c)) must be True
                # contribution to u's sum = f_c * b[c-1] = (1 - e(c)) * b[c-1]
                if b[c-1] == 0:
                    if not (ok0 or ok1):
                        ok = False
                        break
                    # contribution 0 always
                else:
                    if ok0 and ok1:
                        # free: can be 0 (e=1) or 1 (e=0)
                        free_count += 1
                    elif ok0:
                        # e(c)=0, contributes 1
                        forced_sum ^= 1
                    elif ok1:
                        # e(c)=1, contributes 0
                        pass
                    else:
                        ok = False
                        break
            if not ok:
                if e == 0: dp0[u] = False
                else: dp1[u] = False
                continue
            target = (1 - b[u-1] - e*bp) % 2
            if free_count > 0:
                feasible = True
            else:
                feasible = (forced_sum == target)
            if e == 0:
                dp0[u] = feasible
            else:
                dp1[u] = feasible
    
    # Check root
    if not dp0[1]:
        print("NO")
        return
    
    # Reconstruct: top-down
    # For each node, given e, determine f_c for each child
    chosen_e = [0]*(n+1)  # e value for each node
    chosen_e[1] = 0
    # Process in BFS/DFS order (top-down)
    edge_orient = {}  # (u, v) -> first removed
    
    for u in order:  # forward order (root first)
        e = chosen_e[u]
        bp = b[parent[u]-1] if parent[u] != -1 else 0
        target = (1 - b[u-1] - e*bp) % 2
        
        # Determine f_c for each child
        # Strategy: assign forced first, then handle free
        f_choices = {}
        forced_sum = 0
        free_children = []
        for c in children[u]:
            ok0 = dp0[c]
            ok1 = dp1[c]
            if b[c-1] == 0:
                # contribution 0, but still must pick valid e(c)
                # prefer either; say prefer e(c)=0 if dp0, else 1
                if ok0:
                    f_choices[c] = 1  # f_c=1, e(c)=0
                else:
                    f_choices[c] = 0  # f_c=0, e(c)=1
            else:
                if ok0 and ok1:
                    free_children.append(c)
                    # default: e(c)=1, f_c=0, contribution 0
                    f_choices[c] = 0
                elif ok0:
                    f_choices[c] = 1  # contribution 1
                    forced_sum ^= 1
                else:  # ok1
                    f_choices[c] = 0  # contribution 0
        
        current_sum = forced_sum
        if current_sum != target:
            # need to flip one free child
            if free_children:
                c = free_children[0]
                f_choices[c] = 1  # contribution 1, e(c)=0
                current_sum ^= 1
        # current_sum should equal target now
        
        for c in children[u]:
            fc = f_choices[c]
            ec = 1 - fc
            chosen_e[c] = ec
            # edge between u and c: if fc=1, c removed after u, so u first
            edge_orient[(u, c)] = (u if fc == 1 else c)
    
    # Build DAG: for each edge, first removed -> later removed
    # Topological order
    indeg = [0]*(n+1)
    dag = [[] for _ in range(n+1)]
    for (u, c), first in edge_orient.items():
        later = c if first == u else u
        dag[first].append(later)
        indeg[later] += 1
    
    from collections import deque
    q = deque()
    for i in range(1, n+1):
        if indeg[i] == 0:
            q.append(i)
    result = []
    while q:
        u = q.popleft()
        result.append(u)
        for v in dag[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    
    print("YES")
    print(*result)

t = int(input())
for _ in range(t):
    solve()
