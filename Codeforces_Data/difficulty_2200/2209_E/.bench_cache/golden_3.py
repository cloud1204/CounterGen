import sys
import heapq

def z_function(s):
    n = len(s)
    z = [0]*n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r-i, z[i-l])
        while i+z[i] < n and s[z[i]] == s[i+z[i]]:
            z[i] += 1
        if i+z[i] > r:
            l, r = i, i+z[i]
    return z

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    t = int(input_data[idx]); idx+=1
    out = []
    for _ in range(t):
        n, q = int(input_data[idx]), int(input_data[idx+1]); idx+=2
        s = input_data[idx].decode(); idx+=1
        queries = []
        for _ in range(q):
            l, r = int(input_data[idx]), int(input_data[idx+1]); idx+=2
            queries.append((l,r))
        for l, r in queries:
            T = s[l-1:r]
            L = len(T)
            z = z_function(T)
            dp = [0]*(L+1)
            heap = []
            # p=0 always valid
            heapq.heappush(heap, (-dp[0], L, 0))  # exp = 0 + z[0] = L (treating z[0]=L)
            total = 0
            for i in range(1, L+1):
                # add p = i-1
                p = i-1
                if p >= 1:
                    exp_p = p + z[p]
                    if exp_p >= i:  # otherwise it's already expired
                        heapq.heappush(heap, (-dp[p], exp_p, p))
                # remove expired
                while heap and heap[0][1] < i:
                    heapq.heappop(heap)
                dp[i] = -heap[0][0] + 1
                total += dp[i]
            out.append(str(total))
    print('\n'.join(out))

solve()
