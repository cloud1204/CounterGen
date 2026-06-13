def solve(n):
    if n < 3:
        return 0
    count = 0
    
    divisors = []
    i = 1
    while i*i <= n:
        if n % i == 0:
            divisors.append(i)
            if i != n//i:
                divisors.append(n//i)
        i += 1
    
    for d in divisors:
        if d >= 3:
            b = d - 1
            q = n // d
            if 1 <= q <= b-1 and b >= 2:
                count += 1
    
    for p in range(2, 45):
        if p == 2:
            b_max = int(n**0.5) + 2
        else:
            b_max = int(n**(1.0/p)) + 2
        for b in range(2, b_max+1):
            bp = b**p
            if bp > n:
                break
            S = (bp - 1) // (b - 1)
            if S > n:
                continue
            if n % S != 0:
                continue
            m = n // S
            B = bp
            digits_ok = True
            has_leading = False
            while m > 0:
                d = m % B
                if d >= b:
                    digits_ok = False
                    break
                m //= B
                if m == 0:
                    if d == 0:
                        digits_ok = False
                    else:
                        has_leading = True
            if digits_ok and has_leading:
                k_total_digits = 0
                pass
            if digits_ok and has_leading:
                m2 = n // S
                k = 0
                while m2 > 0:
                    k += 1
                    m2 //= B
                if k >= 2:
                    count += 1
    
    return count
