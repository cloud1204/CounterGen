def solve():
    n = int(input())
    a = list(map(int, input().split()))
    MOD = 10**9 + 7
    count = 0
    from itertools import product
    for b in product(range(n+1), repeat=n):
        ok = True
        for i in range(1, n+1):
            k = n - i + 1
            S = list(b[:i])
            present = set(S)
            missing = []
            v = 0
            while len(missing) < k:
                if v not in present:
                    missing.append(v)
                v += 1
            if missing[-1] != a[i-1]:
                ok = False
                break
        if ok:
            count += 1
    print(count % MOD)

t = int(input())
for _ in range(t):
    solve()
