def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    from collections import defaultdict
    dp = defaultdict(set)
    dp[0].add(tuple([0]*k))
    for mask in range(1<<n):
        if mask not in dp: continue
        for state in dp[mask]:
            for i in range(n):
                if not (mask >> i) & 1:
                    new_state = list(state)
                    new_state[0] += a[i]  # min is at index 0
                    new_state.sort()
                    dp[mask | (1<<i)].add(tuple(new_state))
    ans = 0
    full = (1<<n) - 1
    for state in dp[full]:
        ans = max(ans, max(state))
    print(ans)
