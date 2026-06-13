import sys
from math import comb

MOD = 998244353

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(input_data[idx]); idx+=1
    m = int(input_data[idx]); idx+=1
    cnt = [0]*61
    for i in range(n):
        c = int(input_data[idx]); idx+=1
        cnt[c] += 1
    
    out = []
    for _ in range(m):
        t = int(input_data[idx]); idx+=1
        x = int(input_data[idx]); idx+=1
        if t == 1:
            cnt[x] += 1
        elif t == 2:
            cnt[x] -= 1
        else:
            if x > 200:
                out.append(0)
                continue
            MAXCAP = 200
            # dp[s][cap] = ways
            dp = [[0]*(MAXCAP+1) for _ in range(7)]
            dp[0][0] = 1
            for v in range(60, -1, -1):
                c = cnt[v]
                new_dp = [[0]*(MAXCAP+1) for _ in range(7)]
                # precompute suffix sum of binomials
                binoms = [comb(c, k) % MOD for k in range(c+1)]
                suffix = [0]*(c+2)
                for k in range(c, -1, -1):
                    suffix[k] = (suffix[k+1] + binoms[k]) % MOD
                pow2c = pow(2, c, MOD)
                for s in range(7):
                    for cap in range(MAXCAP+1):
                        if dp[s][cap] == 0:
                            continue
                        val = dp[s][cap]
                        if s == 6:
                            new_dp[6][cap] = (new_dp[6][cap] + val * pow2c) % MOD
                        else:
                            need = 6 - s
                            max_j = min(c, need)
                            cur_cap = cap
                            for j in range(0, max_j+1):
                                if j > 0:
                                    add = v >> (s + j - 1)
                                    cur_cap += add
                                    if cur_cap > MAXCAP:
                                        cur_cap = MAXCAP + 100
                                ns = s + j
                                if cur_cap > MAXCAP:
                                    continue
                                if j < need:
                                    ways = binoms[j]
                                else:
                                    ways = suffix[j]
                                new_dp[ns][cur_cap] = (new_dp[ns][cur_cap] + val * ways) % MOD
                dp = new_dp
            # sum over cap >= x
            ans = 0
            for s in range(7):
                for cap in range(x, MAXCAP+1):
                    ans = (ans + dp[s][cap]) % MOD
            out.append(ans)
    print('\n'.join(map(str, out)))

solve()
