def solve(n):
    if n < 3: return 0  # smallest tidy is n=S with k=1,p=2,b=2: 1+2=3
    count = 0
    # p=2
    divs = get_divisors(n)
    for d in divs:
        if d >= 3:
            b = d - 1
            if b >= 2:
                m = n // d
                B = b*b
                ok = True
                while m > 0:
                    if m % B >= b:
                        ok = False; break
                    m //= B
                if ok:
                    count += 1
    # p >= 3
    p = 3
    while True:
        # b >= 2, S = 1+b+...+b^(p-1) >= 1+2+...+2^(p-1) = 2^p - 1
        if (1 << p) - 1 > n: break
        b = 2
        while True:
            # compute S
            S = 0
            bp = 1
            for _ in range(p):
                S += bp
                bp *= b
            if S > n: break
            if n % S == 0:
                m = n // S
                B = bp  # b^p
                ok = True
                while m > 0:
                    if m % B >= b:
                        ok = False; break
                    m //= B
                if ok:
                    count += 1
            b += 1
        p += 1
    return count
