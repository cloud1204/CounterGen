import sys
from itertools import product

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    MOD = 10**9+7
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx+=1
        a = [int(input_data[idx+i]) for i in range(n+1)]
        idx += n+1
        # determine undetermined positions
        undet = [i for i in range(n+1) if a[i]==-1]
        # check determined values are in [0,n]
        valid_fixed = True
        for i in range(n+1):
            if a[i] != -1:
                if a[i] < 0 or a[i] > n:
                    valid_fixed = False
                    break
                if i == n and a[i] == 0:
                    valid_fixed = False
                    break
        if not valid_fixed:
            out.append('0')
            continue
        count = 0
        # enumerate
        # For each undetermined, value in [0,n], but for position n, value in [1,n]
        ranges = []
        for i in undet:
            if i == n:
                ranges.append(range(1, n+1))
            else:
                ranges.append(range(0, n+1))
        for combo in product(*ranges):
            b = a[:]
            for j, pos in enumerate(undet):
                b[pos] = combo[j]
            # check cool
            # compute g coefficients
            # g(x) = sum i * x^{b[i]}
            # so for each k in [0,n], coeff = sum i where b[i]=k
            ok = True
            s = [0]*(n+1)
            for i in range(n+1):
                v = b[i]
                if v > n:
                    ok = False
                    break
                s[v] += i
            if not ok:
                continue
            # also g may have terms with x^v for v > n, those are nonzero if any i>=1 with b[i]=v
            # but we've restricted b[i] <= n
            if all(b[k] == s[k] for k in range(n+1)):
                count += 1
        out.append(str(count % MOD))
    print('\n'.join(out))

solve()
