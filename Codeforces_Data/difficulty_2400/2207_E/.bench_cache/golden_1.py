import sys
from itertools import product

def kmex(S, k):
    s = set(S)
    count = 0
    i = 0
    while True:
        if i not in s:
            count += 1
            if count == k:
                return i
        i += 1

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 10**9 + 7
    results = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        
        for i in range(n):
            k = n - i + 1
            if a[i] > i + (k - 1):
                pass
        
        count = 0
        valid_a = True
        for i in range(n):
            k = n - i + 1
            if a[i] < k - 1:
                valid_a = False
                break
            if a[i] > i + (k - 1):
                pass
        
        if not valid_a:
            results.append(0)
            continue
        
        for b in product(range(n+1), repeat=n):
            ok = True
            for i in range(n):
                k = n - i + 1
                if kmex(b[:i+1], k) != a[i]:
                    ok = False
                    break
            if ok:
                count += 1
        
        results.append(count % MOD)
    
    print('\n'.join(map(str, results)))

solve()
