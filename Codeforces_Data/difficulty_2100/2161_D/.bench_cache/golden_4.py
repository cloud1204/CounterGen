import sys
from bisect import bisect_left

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        a = [int(x) for x in input_data[idx:idx+n]]
        idx += n
        # group positions by value, 1-indexed positions
        P = [[] for _ in range(n+2)]  # values 1..n
        for i, x in enumerate(a):
            P[x].append(i+1)
        # Process from v=n down to 1
        H = [0] * (n+2)  # H[n+1] = 0
        B = [None] * (n+2)  # B[v] = list of prefix maxes
        # We'll need to evaluate f(v, M) given B[v] and H[v+1] structure.
        # f(v, M): J = bisect_left(P[v], M); if J==0 return H[v+1]; else max(H[v+1], (J+1) + B[v][J-1]) -- careful indexing
        # Let me use B[v] as 1-indexed list where B[v][j] = max_{i=1..j}(c_i - i). Store as list of length k+1 with B[v][0] = -inf.
        
        def eval_f(v, M):
            if v > n:
                return 0
            pos = P[v]
            J = bisect_left(pos, M)
            if J == 0:
                return H[v+1]
            # max(H[v+1], (J+1) + B[v][J])
            return max(H[v+1], (J+1) + B[v][J])
        
        for v in range(n, 0, -1):
            pos = P[v]
            k = len(pos)
            if k == 0:
                H[v] = H[v+1]
                B[v] = [float('-inf')]
                continue
            # compute c_i = eval_f(v+1, pos[i-1]) for i in 1..k
            Bv = [float('-inf')] * (k+1)
            cur_max = float('-inf')
            for i in range(1, k+1):
                c = eval_f(v+1, pos[i-1])
                val = c - i
                if val > cur_max:
                    cur_max = val
                Bv[i] = cur_max
            B[v] = Bv
            H[v] = max(H[v+1], (k+1) + Bv[k])
        
        kept = H[1]
        out.append(str(n - kept))
    print('\n'.join(out))

solve()
