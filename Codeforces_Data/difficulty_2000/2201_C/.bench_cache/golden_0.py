import sys
from itertools import combinations

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 998244353
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        S = input_data[idx]; idx += 1
        count = 0
        arr = list(S)
        for mask in range(1, 1 << n):
            chosen = []
            for i in range(n):
                if mask & (1 << i):
                    chosen.append(i)
            k = len(chosen)
            new_arr = arr[:]
            chars = [arr[i] for i in chosen]
            for j in range(k):
                new_arr[chosen[j]] = chars[(j - 1) % k]
            bal = 0
            ok = True
            for c in new_arr:
                if c == '(':
                    bal += 1
                else:
                    bal -= 1
                if bal < 0:
                    ok = False
                    break
            if ok and bal == 0:
                count += 1
        results.append(count % MOD)
    print('\n'.join(map(str, results)))

solve()
