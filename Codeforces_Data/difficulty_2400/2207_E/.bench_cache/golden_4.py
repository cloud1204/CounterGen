import sys
from itertools import product

def kmex(arr, k):
    s = set(arr)
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
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        count = 0
        for b in product(range(n+1), repeat=n):
            ok = True
            for i in range(n):
                if kmex(b[:i+1], n-i) != a[i]:
                    ok = False
                    break
            if ok:
                count += 1
        print(count % MOD)

solve()
