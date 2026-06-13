import sys
input = sys.stdin.readline

def solve():
    MOD = 10**9 + 7
    t = int(input())
    results = []
    for _ in range(t):
        n, x = map(int, input().split())
        ops = input().split()
        a_list = []
        b_list = []
        for op in ops:
            sym = op[0]
            y = int(op[1:])
            if sym == '+':
                a_list.append(1)
                b_list.append(y % MOD)
            elif sym == '-':
                a_list.append(1)
                b_list.append((-y) % MOD)
            elif sym == 'x':
                a_list.append(y % MOD)
                b_list.append(0)
            else:
                a_list.append(pow(y % MOD, MOD-2, MOD))
                b_list.append(0)
        
        A = 1
        for a in a_list:
            A = A * a % MOD
        
        P = [0] * (n + 1)
        P[0] = 1
        deg = 0
        for a in a_list:
            for j in range(deg + 1, 0, -1):
                P[j] = (P[j] + a * P[j-1]) % MOD
            deg += 1
        
        sum_b = 0
        for b in b_list:
            sum_b = (sum_b + b) % MOD
        
        ans = A * (x % MOD) % MOD
        
        if sum_b != 0:
            Q = [0] * n
            Q[0] = P[0]
            for i in range(1, n):
                Q[i] = (P[i] - Q[i-1]) % MOD
            
            fact = [1] * (n + 1)
            for i in range(1, n + 1):
                fact[i] = fact[i-1] * i % MOD
            inv_fact = [1] * (n + 1)
            inv_fact[n] = pow(fact[n], MOD-2, MOD)
            for i in range(n-1, -1, -1):
                inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
            
            T = 0
            for m in range(n):
                comb = fact[n-1] * inv_fact[m] % MOD * inv_fact[n-1-m] % MOD
                inv_comb = pow(comb, MOD-2, MOD)
                T = (T + Q[m] * inv_comb) % MOD
            
            inv_n = pow(n, MOD-2, MOD)
            ans = (ans + sum_b * T % MOD * inv_n) % MOD
        
        results.append(ans % MOD)
    
    print('\n'.join(map(str, results)))

solve()
