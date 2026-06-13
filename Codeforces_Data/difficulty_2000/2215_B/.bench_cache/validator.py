def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.strip().split('\n')
        idx = 0
        if idx >= len(lines):
            return "invalid: missing t"
        t_parts = lines[idx].split()
        if len(t_parts) != 1:
            return "invalid: first line must contain only t"
        try:
            t = int(t_parts[0])
        except ValueError:
            return "invalid: t is not an integer"
        idx += 1
        if t < 1 or t > 1000:
            return "invalid: t out of range (1 <= t <= 1000)"
        
        total_n = 0
        for tc in range(t):
            if idx >= len(lines):
                return f"invalid: missing n for test case {tc+1}"
            n_parts = lines[idx].split()
            if len(n_parts) != 1:
                return f"invalid: n line must contain only n for test case {tc+1}"
            try:
                n = int(n_parts[0])
            except ValueError:
                return f"invalid: n is not an integer for test case {tc+1}"
            idx += 1
            if n < 1 or n > 5000:
                return f"invalid: n out of range (1 <= n <= 5000) for test case {tc+1}"
            total_n += n
            if total_n > 5000:
                return "invalid: sum of n over all test cases exceeds 5000"
            
            if idx >= len(lines):
                return f"invalid: missing p for test case {tc+1}"
            p_parts = lines[idx].split()
            if len(p_parts) != n:
                return f"invalid: p must have exactly n integers for test case {tc+1}"
            try:
                p = [int(x) for x in p_parts]
            except ValueError:
                return f"invalid: p contains non-integer for test case {tc+1}"
            idx += 1
            if sorted(p) != list(range(1, n+1)):
                return f"invalid: p is not a permutation of 1..n for test case {tc+1}"
            
            if idx >= len(lines):
                return f"invalid: missing d for test case {tc+1}"
            d_parts = lines[idx].split()
            if len(d_parts) != n:
                return f"invalid: d must have exactly n integers for test case {tc+1}"
            try:
                d = [int(x) for x in d_parts]
            except ValueError:
                return f"invalid: d contains non-integer for test case {tc+1}"
            idx += 1
            for di in d:
                if di < 0 or di > n:
                    return f"invalid: d_i out of range (0 <= d_i <= n) for test case {tc+1}"
        
        if idx != len(lines):
            extra = [l for l in lines[idx:] if l.strip()]
            if extra:
                return "invalid: extra data after expected input"
        
        return "valid"
    except Exception as e:
        return f"invalid: parsing error {e}"
