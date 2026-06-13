import sys
from sys import setrecursionlimit
from collections import defaultdict, deque

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        k = int(input_data[idx]); idx+=1
        v0 = int(input_data[idx]); idx+=1
        adj = [[] for _ in range(n+1)]
        edges = []
        for i in range(n-1):
            a = int(input_data[idx]); idx+=1
            b = int(input_data[idx]); idx+=1
            edges.append((a,b))
            adj[a].append((b, i))
            adj[b].append((a, i))
        leaves = [u for u in range(1, n+1) if len(adj[u])==1]
        is_leaf = [False]*(n+1)
        for u in leaves: is_leaf[u]=True
        
        # States: (vertex, blocked_edge_id (-1 for none), cooldown, turn)
        # turn: 0=Snorlax, 1=Cyndaquil
        # cooldown in [0, k]
        # encode state as integer
        # Total states: n * n * (k+1) * 2
        NE = n  # edges 0..n-2, plus -1 → use n-1 for no_block, edge ids 0..n-2
        NO_BLOCK = n-1
        
        def enc(v, b, cd, t):
            return ((v*NE + b)*(k+1) + cd)*2 + t
        
        total = (n+1)*NE*(k+1)*2
        # WIN[state] = True means Cyndaquil wins
        WIN = [False]*total
        # successors count for Snorlax turn states (need all to be WIN)
        snorlax_total = {}
        snorlax_remaining = [0]*total
        
        # Build state space by enumeration would be too much. Let's use BFS from WIN states (leaves) backward.
        # But we need reverse graph. Let's build forward graph and reverse it.
        # That's expensive. Alternative: iterate.
        
        # Iterative fixed point:
        # For Cyndaquil-turn states: WIN if v is leaf or any successor is WIN.
        # For Snorlax-turn states: WIN if all successors are WIN.
        
        # Initialize
        # Find all reachable states from initial state via forward search, then do game-solving on subgraph.
        
        start = enc(v0, NO_BLOCK, 0, 0)
        # forward exploration
        visited = set()
        stack = [start]
        visited.add(start)
        all_states = []
        successors = {}
        while stack:
            s = stack.pop()
            all_states.append(s)
            t = s % 2
            cd = (s//2) % (k+1)
            b = (s//(2*(k+1))) % NE
            v = s//(2*(k+1)*NE)
            succs = []
            if t == 0:  # Snorlax's turn
                # option 1: do nothing
                ns = enc(v, b, cd, 1)
                succs.append(ns)
                # option 2: if cd <= 0, block any edge
                if cd <= 0:
                    for i in range(n-1):
                        ns = enc(v, i, k, 1)
                        succs.append(ns)
            else:  # Cyndaquil's turn
                new_cd = max(0, cd-1)  # cap at 0 since cd<=0 same as 0
                # Actually the problem: cd decreases by 1 after Cyndaquil's turn. New cd could be negative but we cap.
                # Stay
                ns = enc(v, b, new_cd, 0)
                succs.append(ns)
                # Move to neighbor
                for (u, eid) in adj[v]:
                    if eid != b:
                        ns = enc(u, b, new_cd, 0)
                        succs.append(ns)
            successors[s] = succs
            for ns in succs:
                if ns not in visited:
                    visited.add(ns)
                    stack.append(ns)
        
        # Now solve via fixed point
        WIN = {}
        # Reverse adjacency
        predecessors = defaultdict(list)
        for s, succs in successors.items():
            for ns in succs:
                predecessors[ns].append(s)
        
        queue = deque()
        # Initialize Cyndaquil-turn leaf states as WIN
        for s in visited:
            t = s % 2
            cd = (s//2) % (k+1)
            b = (s//(2*(k+1))) % NE
            v = s//(2*(k+1)*NE)
            if t == 1 and is_leaf[v]:
                WIN[s] = True
                queue.append(s)
        
        # Counts for Snorlax turn
        remaining = {}
        for s in visited:
            t = s % 2
            if t == 0:
                remaining[s] = len(successors[s])
        
        while queue:
            s = queue.popleft()
            for ps in predecessors[s]:
                if ps in WIN: continue
                t = ps % 2
                if t == 1:  # Cyndaquil turn: any succ wins → win
                    WIN[ps] = True
                    queue.append(ps)
                else:  # Snorlax turn: needs all
                    remaining[ps] -= 1
                    if remaining[ps] == 0:
                        WIN[ps] = True
                        queue.append(ps)
        
        out.append("YES" if WIN.get(start, False) else "NO")
    
    print('\n'.join(out))

solve()
