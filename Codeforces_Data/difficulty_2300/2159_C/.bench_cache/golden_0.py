
def solve():
    n = int(input())
    a = list(map(int, input().split()))
    MOD = 10**9 + 7
    
    in_T = [False]*(n+1)  # forced in T
    out_T = [False]*(n+1)  # forced out
    paired = [0]*(n+1)  # partner if forced paired
    
    for i in range(1, n):
        if a[i] == -1: continue
        if a[i] == 0:
            out_T[i] = True
        elif 1 <= a[i] <= n:
            v = a[i]
            in_T[i] = True
            in_T[v] = True
            # check pair
            if paired[i] != 0 and paired[i] != v: return 0
            if paired[v] != 0 and paired[v] != i: return 0
            paired[i] = v
            paired[v] = i
        else:
            return 0
    
    # Now check: for v that's forced in T (and not = 0), if a[v] is set, consistency was checked.
    # Also out_T and in_T conflict?
    for i in range(1, n+1):
        if in_T[i] and out_T[i]: return 0
    
    # Special: n must be in T (b_n != 0). So if out_T[n], return 0. n=a[n]=-1, so out_T[n]=False unless... no.
    # But we need n ∈ T. n is forced in only if it's mentioned in a pair. Otherwise it's "free but must be in T".
    
    # Now collect free elements. Free = not in_T and not out_T.
    # n: if n is not in_T, we need to force it. But if a[n]=-1, n is free. We must include n in T.
    
    # Let me think of "free" elements; among them, those that join T must be paired (or fixed point) among themselves (or with other free elements).
    
    # Process: elements in_T and not paired correctly?
    # Actually all in_T elements have a partner (paired[i] != 0). Self-loop means paired[i] = i.
    # These are determined: they're in T with their partner determined.
    
    # The rest are free. Let free = [i for i in 1..n if not in_T[i] and not out_T[i]]
    # We must put n in T if n is free (it must be in T).
    
    # Wait n might be in_T already (if some a[i] = n was set). Then it's already in T.
    
    # If n is free (not in_T), we need to force it in T but it can pair with anyone.
    
    # For free elements: choose subset S ⊆ free that go into T (S must contain n if n is free, otherwise n is already in_T).
    # Among S, they pair up with involution. Number of involutions on a set of size k is the telephone number T(k) = sum_{j} C(k, 2j) * (2j-1)!!.
    
    # If n is free and must be in T: number of ways = sum over S containing n, S ⊆ free, with involution count on S.
    
    # Equivalently, fix n in T, then choose any subset of (free \ {n}) to also be in T, and count involutions on that augmented set.
    
    # Let m = |free|. If n is free: we need n in T, free others can be in/out. So for k = 0..m-1 (number of additional free in T), count = C(m-1, k) * involutions(k+1).
    # If n is not free (i.e., in_T), then free elements can each be in/out. Sum over k from 0 to m: C(m,k) * involutions(k).
    
    # involutions(k) = number of involutions on k elements = T(k), telephone number.
    # Recurrence: T(0)=1, T(1)=1, T(k) = T(k-1) + (k-1)*T(k-2).
