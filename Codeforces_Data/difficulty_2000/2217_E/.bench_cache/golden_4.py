import sys
from math import isqrt

def solve(n):
    if n == 1:
        return 0
    S = isqrt(n)
    count = 0
    # b from 2 to S
    for b in range(2, S+1):
        # compute digits of n in base b
        digits = []
        x = n
        while x > 0:
            digits.append(x % b)
            x //= b
        L = len(digits)
        if L < 2:
            continue
        # find divisors p of L with p>=2
        for p in range(2, L+1):
            if L % p == 0:
                ok = True
                for i in range(0, L, p):
                    d = digits[i]
                    for j in range(1, p):
                        if digits[i+j] != d:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    count += 1
    # b > S, L=2 case
    # b = m-1, m | n, m >= S+2, m <= n, d=n/m, 1<=d<=m-2
    # find divisors of n
    divs = []
    i = 1
    while i*i <= n:
        if n % i == 0:
            divs.append(i)
            if i != n//i:
                divs.append(n//i)
        i += 1
    for m in divs:
        b = m - 1
        if b <= S:
            continue
        if b < 2:
            continue
        d = n // m
        if 1 <= d <= b-1:
            count += 1
    return count

t = int(input())
for _ in range(t):
    n = int(input())
    print(solve(n))
