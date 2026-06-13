import sys
from sys import stdin

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 998244353
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        T = list(map(int, input_data[idx:idx+n])); idx += n
        if n == 1:
            out.append("1")
            continue
        seen = set()
        for mask in range(1 << (n-1)):
            # cuts after position k (1-indexed) if bit k-1 set
            blocks = []
            start = 0
            for k in range(n-1):
                if mask & (1 << k):
                    blocks.append((start, k))  # 0-indexed inclusive
                    start = k+1
            blocks.append((start, n-1))
            S = []
            for (l, r) in blocks:
                for i in range(r, l-1, -1):
                    S.append(T[i])
            seen.add(tuple(S))
        out.append(str(len(seen) % MOD))
    print("\n".join(out))

solve()
