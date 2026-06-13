import sys
from sys import stdin

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n, k = int(input_data[idx]), int(input_data[idx+1]); idx += 2
        a = [int(input_data[idx+i]) for i in range(n)]; idx += n
        
        # dp[mask] = set of sorted tuples of bin sums (k bins) achievable
        dp = [set() for _ in range(1 << n)]
        dp[0].add(tuple([0]*k))
        
        best = 0
        for mask in range(1 << n):
            for b in dp[mask]:
                if mask == (1 << n) - 1:
                    if b[-1] > best:
                        best = b[-1]
                    continue
                for i in range(n):
                    if not (mask & (1 << i)):
                        # add a[i] to b[0] (the min)
                        new_b = list(b[1:]) + [b[0] + a[i]]
                        new_b.sort()
                        dp[mask | (1 << i)].add(tuple(new_b))
        
        out.append(str(best))
    
    print('\n'.join(out))

solve()
