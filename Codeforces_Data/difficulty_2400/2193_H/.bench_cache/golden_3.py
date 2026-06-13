import sys
from sys import setrecursionlimit
from collections import deque

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        b = [x % 2 for x in a]
        adj = [[] for _ in range(n+1)]
        for _ in range(n-1):
            u = int(input_data[idx]); idx += 1
            v = int(input_data[idx]); idx += 1
            adj[u].append(v)
            adj[v].append(u)
        
        if n == 1:
            if b[0] == 1:
                out.append("YES")
                out.append("1")
            else:
                out.append("NO")
            continue
        
        # Root at 1 (1-indexed)
        parent = [0] * (n+1)
        order = []
        visited = [False] * (n+1)
        # BFS
        q = deque([1])
        visited[1] = True
        parent[1] = 0
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    q.append(v)
        
        children = [[] for _ in range(n+1)]
        for v in range(2, n+1):
            children[parent[v]].append(v)
        
        # f[v] = (set of valid p_v, dict from p_v to dict {child: p_c})
        # since p_v in {0,1}, store as list of 2 entries.
        # valid[v][p_v] = True/False
        # choice[v][p_v] = dict child -> p_c (only when valid)
        valid = [[False, False] for _ in range(n+1)]
        choice = [[None, None] for _ in range(n+1)]
        
        # b is 0-indexed; vertices 1..n. Let me use bb[v] = b[v-1].
        bb = [0] * (n+1)
        for v in range(1, n+1):
            bb[v] = b[v-1]
        target = [0] * (n+1)
        for v in range(1, n+1):
            target[v] = 1 - bb[v]
        
        # Process in reverse BFS order
        for v in reversed(order):
            par = parent[v]
            parent_b = bb[par] if par != 0 else 0
            ch = children[v]
            
            for p_v in [0, 1]:
                if v == 1 and p_v == 1:
                    # no parent, set p_v=0 by convention
                    continue
                # Compute needed
                # constraint at v: sum_{c in children, b_c=1}[p_c=0] + [parent_b=1][p_v=0] ≡ target_v
                # i.e., sum ≡ target_v - parent_b * (1 if p_v==0 else 0) mod 2
                
                needed = (target[v] - parent_b * (1 if p_v == 0 else 0)) % 2
                
                forced_sum = 0
                free_children = []
                child_choice = {}
                possible = True
                for c in ch:
                    if not valid[c][0] and not valid[c][1]:
                        possible = False
                        break
                    if bb[c] == 0:
                        # doesn't affect, but pick any valid p_c
                        if valid[c][0]:
                            child_choice[c] = 0
                        else:
                            child_choice[c] = 1
                    else:
                        # b_c == 1
                        if valid[c][0] and valid[c][1]:
                            free_children.append(c)
                        elif valid[c][0]:
                            child_choice[c] = 0
                            forced_sum += 1
                        elif valid[c][1]:
                            child_choice[c] = 1
                
                if not possible:
                    continue
                
                diff = (needed - forced_sum) % 2
                
                if diff == 0:
                    # all free children: pick p_c=1 (contributes 0)
                    for c in free_children:
                        child_choice[c] = 1
                    valid[v][p_v] = True
                    choice[v][p_v] = child_choice
                else:
                    if len(free_children) >= 1:
                        # set one free child to p_c=0 (contributes 1)
                        c0 = free_children[0]
                        child_choice[c0] = 0
                        for c in free_children[1:]:
                            child_choice[c] = 1
                        valid[v][p_v] = True
                        choice[v][p_v] = child_choice
        
        # Check root
        if not valid[1][0]:
            out.append("NO")
            continue
        
        # Reconstruct: assign p_v for all v
        p = [0] * (n+1)
        # p[1] = 0 (irrelevant)
        # BFS from root, assigning children's p based on choice
        stack = [1]
        p[1] = 0
        # Use the choice for root with p_v=0
        # For each v, after p_v determined, use choice[v][p_v] for children
        from collections import deque
        dq = deque([1])
        while dq:
            v = dq.popleft()
            ch_choice = choice[v][p[v] if v != 1 else 0]
            if ch_choice is None:
                # shouldn't happen
                break
            for c in children[v]:
                p[c] = ch_choice[c]
                dq.append(c)
        
        # Build precedence DAG: for v != root, p[v]=1 means v removed before parent → edge v -> parent
        # Topological sort
        indeg = [0] * (n+1)
        dag = [[] for _ in range(n+1)]
        for v in range(2, n+1):
            par = parent[v]
            if p[v] == 1:
                # v before par
                dag[v].append(par)
                indeg[par] += 1
            else:
                dag[par].append(v)
                indeg[v] += 1
        
        # Kahn
        q = deque()
        for v in range(1, n+1):
            if indeg[v] == 0:
                q.append(v)
        result = []
        while q:
            v = q.popleft()
            result.append(v)
            for u in dag[v]:
                indeg[u] -= 1
                if indeg[u] == 0:
                    q.append(u)
        
        if len(result) != n:
            out.append("NO")
        else:
            out.append("YES")
            out.append(" ".join(map(str, result)))
    
    sys.stdout.write("\n".join(out) + "\n")

solve()
