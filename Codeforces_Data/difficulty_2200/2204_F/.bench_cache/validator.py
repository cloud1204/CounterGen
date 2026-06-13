def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.strip().split('\n')
        if len(lines) != 3:
            return "invalid: expected exactly 3 lines"
        
        first_line = lines[0].split()
        if len(first_line) != 2:
            return "invalid: first line must contain exactly 2 integers"
        
        try:
            n = int(first_line[0])
            m = int(first_line[1])
        except ValueError:
            return "invalid: n and m must be integers"
        
        if not (1 <= n <= 5 * 10**5):
            return "invalid: n must satisfy 1 <= n <= 5*10^5"
        if not (1 <= m <= 5 * 10**5):
            return "invalid: m must satisfy 1 <= m <= 5*10^5"
        
        a_tokens = lines[1].split()
        if len(a_tokens) != n:
            return "invalid: second line must contain exactly n integers"
        
        try:
            a = [int(x) for x in a_tokens]
        except ValueError:
            return "invalid: array a must contain integers"
        
        for ai in a:
            if not (1 <= ai <= 10**8):
                return "invalid: each a_i must satisfy 1 <= a_i <= 10^8"
        
        k_tokens = lines[2].split()
        if len(k_tokens) != m:
            return "invalid: third line must contain exactly m integers"
        
        try:
            k = [int(x) for x in k_tokens]
        except ValueError:
            return "invalid: array k must contain integers"
        
        for ki in k:
            if not (0 <= ki <= 10**8):
                return "invalid: each k_i must satisfy 0 <= k_i <= 10^8"
        
        for i in range(1, m):
            if k[i] < k[i-1]:
                return "invalid: array k must be in non-decreasing order"
        
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
