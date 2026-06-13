import sys

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(input_data[idx]); idx += 1
        funcs = []
        for i in range(n):
            a = int(input_data[idx]); idx += 1
            b = int(input_data[idx]); idx += 1
            c = int(input_data[idx]); idx += 1
            funcs.append((a, b, c, i))
        
        sorted_funcs = sorted(funcs, key=lambda x: (x[0], x[1], x[2]))
        
        less = [[False]*n for _ in range(n)]
        for i in range(n):
            ai, bi, ci, _ = sorted_funcs[i]
            for j in range(i+1, n):
                aj, bj, cj, _ = sorted_funcs[j]
                da = aj - ai
                db = bj - bi
                dc = cj - ci
                if da == 0:
                    if db == 0:
                        if dc > 0:
                            less[i][j] = True
                else:
                    if da > 0:
                        disc = db*db - 4*da*dc
                        if disc < 0:
                            less[i][j] = True
        
        dp_in = [1]*n
        for i in range(n):
            best = 0
            for j in range(i):
                if less[j][i] and dp_in[j] > best:
                    best = dp_in[j]
            dp_in[i] = best + 1
        
        dp_out = [1]*n
        for i in range(n-1, -1, -1):
            best = 0
            for j in range(i+1, n):
                if less[i][j] and dp_out[j] > best:
                    best = dp_out[j]
            dp_out[i] = best + 1
        
        ans = [0]*n
        for k in range(n):
            orig_i = sorted_funcs[k][3]
            ans[orig_i] = dp_in[k] + dp_out[k] - 1
        
        out.append(' '.join(map(str, ans)))
    
    sys.stdout.write('\n'.join(out) + '\n')

solve()
