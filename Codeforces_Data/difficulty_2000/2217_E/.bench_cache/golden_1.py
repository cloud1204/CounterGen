def tidiness(n):
    count = 0
    # p = 2: iterate divisors of n
    # find all divisors q of n with q >= 3
    divs = []
    i = 1
    while i*i <= n:
        if n % i == 0:
            divs.append(i)
            if i != n//i:
                divs.append(n//i)
        i += 1
    for q in divs:
        if q < 3: continue
        b = q - 1
        # b >= 2
        m = n // q
        # check m in base b^2 has all digits < b
        B = b * b
        ok = True
        mm = m
        while mm > 0:
            d = mm % B
            if d >= b:
                ok = False
                break
            mm //= B
        if ok:
            count += 1
    
    # p >= 3
    p = 3
    while True:
        # b >= 2, b^(p-1) <= n means b <= n^(1/(p-1))
        # actually need R <= n, R = (b^p-1)/(b-1) >= b^(p-1)
        # so b^(p-1) <= n
        if 2**(p-1) > n:
            break
        # find max b
        b = 2
        while True:
            # compute b^p
            bp = b**p
            R = (bp - 1) // (b - 1)
            if R > n:
                break
            if n % R == 0:
                m = n // R
                B = bp
                ok = True
                mm = m
                while mm > 0:
                    d = mm % B
                    if d >= b:
                        ok = False
                        break
                    mm //= B
                if ok:
                    count += 1
            b += 1
        p += 1
    
    return count
