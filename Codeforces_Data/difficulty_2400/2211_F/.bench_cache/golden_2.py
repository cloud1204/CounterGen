from itertools import combinations_with_replacement

def f(a, k, l, r):
    if k not in a[l-1:r]:
        return 0
    mid = (l+r)//2
    if a[mid-1] == k:
        return 1
    elif a[mid-1] < k:
        return 1 + f(a, k, mid+1, r)
    else:
        return 1 + f(a, k, l, mid-1)

MOD = 676767677
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    total = 0
    for a in combinations_with_replacement(range(1, m+1), n):
        for k in range(1, m+1):
            total += f(list(a), k, 1, n)
    print(total % MOD)
