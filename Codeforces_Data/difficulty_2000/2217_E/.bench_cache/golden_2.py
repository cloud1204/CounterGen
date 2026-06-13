import sys
from math import isqrt

def divisors(n):
    divs = []
    i = 1
    while i*i <= n:
        if n % i == 0:
            divs.append(i)
            if i != n//i:
                divs.append(n//i)
        i += 1
    return divs

def divisors_of(L):
    res = []
    i = 1
    while i*i <= L:
        if L % i == 0:
            res.append(i)
            if i != L//i:
                res.append(L//i)
        i += 1
    return res

def solve(n):
    if n < 3:  # smallest tidy is for n with b,p≥2, n must be ≥ ? smallest is b=2,p=2, n=(11)_2=3 or (1111)_2=15 etc. Actually (11)_2 = 3.
        return 0
    count = 0
    SQ = isqrt(n)
    for b in range(2, SQ+1):
        # compute base-b digits
        digits = []
        x = n
        while x > 0:
            digits.append(x % b)
            x //= b
        L = len(digits)
        if L < 2:
            continue
        for p in divisors_of(L):
            if p < 2:
                continue
            # check blocks of size p uniform
            ok = True
            for i in range(0, L, p):
                d0 = digits[i]
                for j in range(1, p):
                    if digits[i+j] != d0:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                # also leading digit nonzero: digits[L-1] != 0 automatically since it's the top digit
                count += 1
    # L=2 case for b > SQ
    # n = d*(b+1), d in [1, b-1], b > SQ, b ≤ n
    # m = b+1 divides n, m > SQ+1, m ≤ n+1 but m|n so m ≤ n
    divs = divisors(n)
    for m in divs:
        if m <= SQ + 1:
            continue
        if m > n:
            continue
        b = m - 1
        if b < 2:
            continue
        d = n // m
        if 1 <= d <= b - 1:
            count += 1
    return count

t = int(input())
for _ in range(t):
    n = int(input())
    print(solve(n))
