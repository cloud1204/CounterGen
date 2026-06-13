import sys
from itertools import combinations

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    MOD = 998244353
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        s = input_data[idx]; idx+=1
        count = 0
        for k in range(1, n+1):
            for combo in combinations(range(n), k):
                chars = [s[i] for i in combo]
                new_s = list(s)
                new_s[combo[0]] = chars[-1]
                for j in range(1, k):
                    new_s[combo[j]] = chars[j-1]
                bal = 0
                ok = True
                for c in new_s:
                    bal += 1 if c=='(' else -1
                    if bal < 0:
                        ok = False; break
                if ok and bal==0:
                    count += 1
        results.append(count % MOD)
    print('\n'.join(map(str, results)))

solve()
