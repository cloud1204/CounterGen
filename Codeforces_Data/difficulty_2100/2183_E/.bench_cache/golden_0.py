import sys
from fractions import Fraction
from math import lcm

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    t = int(input_data[idx]); idx += 1
    MOD = 998244353
    results = []
    for _ in range(t):
        n, m = int(input_data[idx]), int(input_data[idx+1])
        idx += 2
        a = [int(input_data[idx+i]) for i in range(n)]
        idx += n
        
        # Check fixed elements: strictly increasing where both fixed?
        # We need to fill zeros.
        # Backtracking.
        count = [0]
        ONE = Fraction(1)
        
        def backtrack(pos, prev_val, current_sum, first_val):
            if pos == n:
                # add wrap
                total = current_sum + Fraction(1, lcm(prev_val, first_val))
                if total >= 1:
                    count[0] = (count[0] + 1) % MOD
                return
            # determine range for a[pos]
            lo = prev_val + 1 if pos > 0 else 1
            # also need that remaining positions can fit
            remaining = n - pos - 1
            hi = m - remaining
            
            if a[pos] != 0:
                v = a[pos]
                if v < lo or v > hi:
                    return
                values = [v]
            else:
                values = range(lo, hi + 1)
            
            for v in values:
                if pos == 0:
                    new_sum = Fraction(0)
                    backtrack(1, v, new_sum, v)
                else:
                    term = Fraction(1, lcm(prev_val, v))
                    new_sum = current_sum + term
                    # pruning: upper bound on remaining sum
                    # remaining terms: n - 1 - pos terms before wrap, plus wrap
                    # each <= 1/(v+1), 1/(v+2), ..., plus 1/first_val (for wrap, since lcm(a_n, a_1) >= a_n >= ... or 1/a_1?)
                    # Actually wrap = 1/lcm(a_n, a_1) <= 1/a_n
                    rem = n - 1 - pos
                    ub = Fraction(0)
                    cur = v
                    for j in range(rem):
                        cur += 1
                        ub += Fraction(1, cur)
                    # wrap <= 1/cur (final a_n)
                    ub += Fraction(1, cur if rem > 0 else v)
                    # Hmm if rem=0, then pos == n-1, next call is wrap directly.
                    if new_sum + ub < 1:
                        continue
                    backtrack(pos + 1, v, new_sum, first_val)
        
        backtrack(0, 0, Fraction(0), 0)
        results.append(count[0])
    
    print('\n'.join(map(str, results)))

solve()
