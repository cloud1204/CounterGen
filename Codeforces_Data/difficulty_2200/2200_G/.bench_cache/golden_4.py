import sys

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 10**9 + 7
    results = []
    for _ in range(t):
        n, x = int(input_data[idx]), int(input_data[idx+1])
        idx += 2
        muls = []
        add_sum = 0
        for i in range(n):
            op = input_data[idx]; idx += 1
            sym = op[0]
            y = int(op[1:])
            if sym == '+':
                add_sum = (add_sum + y) % MOD
            elif sym == '-':
                add_sum = (add_sum - y) % MOD
            elif sym == 'x':
                muls.append(y % MOD)
            elif sym == '/':
                muls.append(pow(y % MOD, MOD-2, MOD))
        B = len(muls)
        poly = [1]
        for m in muls:
            new_poly = [0] * (len(poly) + 1)
            for i, v in enumerate(poly):
                new_poly[i] = (new_poly[i] + v) % MOD
                new_poly[i+1] = (new_poly[i+1] + v * m) % MOD
            poly = new_poly
        M_prod = 1
        for m in muls:
            M_prod = (M_prod * m) % MOD
        max_n = B + 1
        fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            fact[i] = fact[i-1] * i % MOD
        inv_fact = [1] * (max_n + 1)
        inv_fact[max_n] = pow(fact[max_n], MOD-2, MOD)
        for i in range(max_n - 1, -1, -1):
            inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
        def C(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a-b] % MOD
        E_add = 0
        for k in range(B + 1):
            term = poly[k] * pow(C(B, k), MOD-2, MOD) % MOD
            E_add = (E_add + term) % MOD
        E_add = E_add * pow(B + 1, MOD-2, MOD) % MOD
        ans = (x % MOD * M_prod + add_sum * E_add) % MOD
        results.append(ans % MOD)
    sys.stdout.write('\n'.join(str(r) for r in results) + '\n')

solve()
