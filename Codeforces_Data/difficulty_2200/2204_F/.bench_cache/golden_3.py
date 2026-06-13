import sys
from bisect import insort

def solve():
    MOD = 998244353
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    n, m = int(input_data[idx]), int(input_data[idx+1]); idx += 2
    a = [int(x) for x in input_data[idx:idx+n]]; idx += n
    ks = [int(x) for x in input_data[idx:idx+m]]; idx += m
    
    out = []
    for k in ks:
        total = 0
        for l in range(n):
            sorted_b = []
            sum_inv = 0  # sum of 1/b_i mod p
            for r in range(l, n):
                insort(sorted_b, a[r])
                # compute MSF
                # find j_max: max j with S_j <= k, S_j = sum (b_i - 1) for first j
                S = 0
                j_max = 0
                sum_b_first = 0  # sum b_i for i <= j_max
                # iterate
                length = len(sorted_b)
                cum = 0
                jm = 0
                for i in range(length):
                    nxt = cum + sorted_b[i] - 1
                    if nxt <= k:
                        cum = nxt
                        jm = i + 1
                    else:
                        break
                # now jm = j_max, cum = S_{j_max}
                # compute sum of 1/b_i for i > jm
                inv_sum = 0
                for i in range(jm, length):
                    inv_sum = (inv_sum + pow(sorted_b[i], MOD-2, MOD)) % MOD
                if jm == 0:
                    # MSF = k/b_1 + sum 1/b_i for all i (including i=0? wait)
                    # Actually (1+k)/b_1 + sum_{i>=2} 1/b_i = 1/b_1 + k/b_1 + sum_{i>=2} 1/b_i
                    # = sum 1/b_i + k/b_1
                    msf = (inv_sum + k * pow(sorted_b[0], MOD-2, MOD)) % MOD
                else:
                    msf = (jm + (k - cum) + inv_sum) % MOD
                total = (total + msf) % MOD
        out.append(total % MOD)
    print('\n'.join(str(x) for x in out))

solve()
