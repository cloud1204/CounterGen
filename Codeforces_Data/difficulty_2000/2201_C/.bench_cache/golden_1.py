import sys
input = sys.stdin.readline

def solve():
    MOD = 998244353
    n = int(input())
    S = input().strip()
    
    p = [0]*(n+1)
    for i in range(1, n+1):
        p[i] = p[i-1] + (1 if S[i-1]=='(' else -1)
    
    # nxt[i] for '(' at position i (1-indexed): smallest x>=i with p[x]<2.
    nxt = [0]*(n+2)
    # Compute for each i, smallest x>=i with p[x]<2
    # Process right to left
    nxt_pos = n+1  # sentinel meaning no such
    # Actually need for each i, smallest x in [i, n] with p[x]<2. 
    # Note p[n]=0<2, so always exists.
    from_right = [n+1]*(n+2)
    for i in range(n, -1, -1):
        if p[i] < 2:
            from_right[i] = i
        else:
            from_right[i] = from_right[i+1]
    
    # Case A
    caseA = 0
    pw = 1  # 2^(i-1)
    for i in range(1, n+1):
        if S[i-1]=='(':
            caseA = (caseA + pw) % MOD
        pw = pw*2 % MOD
    
    # Case B
    events = [[] for _ in range(n+2)]
    active_sum = 0
    prefix_A = 1  # dp[0]
    caseB = 0
    
    for ip in range(1, n+1):
        for v in events[ip]:
            active_sum = (active_sum - v) % MOD
        A = prefix_A
        B = active_sum
        dpi = (A + B) % MOD
        if S[ip-1]==')':
            caseB = (caseB + dpi) % MOD
            prefix_A = (prefix_A + dpi) % MOD
        else:
            active_sum = (active_sum + dpi) % MOD
            nx = from_right[ip]  # smallest x>=ip with p[x]<2
            # event at nx+1
            events[nx+1].append(dpi)
    
    print((caseA + caseB) % MOD)

t = int(input())
for _ in range(t):
    solve()
