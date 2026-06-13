def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return "invalid: empty input"
        
        idx = 0
        first = lines[idx].split()
        if len(first) != 1:
            return "invalid: first line must contain one integer t"
        try:
            t = int(first[0])
        except ValueError:
            return "invalid: t is not an integer"
        if not (1 <= t <= 10**4):
            return "invalid: t must be between 1 and 10^4"
        idx += 1
        
        sum_n = 0
        sum_m = 0
        
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case data"
            parts = lines[idx].split()
            if len(parts) != 2:
                return "invalid: test case header must contain two integers n and m"
            try:
                n = int(parts[0])
                m = int(parts[1])
            except ValueError:
                return "invalid: n or m is not an integer"
            if not (2 <= n <= 3 * 10**5):
                return "invalid: n must be between 2 and 3*10^5"
            if not (1 <= m <= 3 * 10**5):
                return "invalid: m must be between 1 and 3*10^5"
            sum_n += n
            sum_m += m
            if sum_n > 3 * 10**5:
                return "invalid: sum of n across test cases exceeds 3*10^5"
            if sum_m > 3 * 10**5:
                return "invalid: sum of m across test cases exceeds 3*10^5"
            idx += 1
            
            for j in range(m):
                if idx >= len(lines):
                    return "invalid: missing constraint line"
                cparts = lines[idx].split()
                if len(cparts) != 2:
                    return "invalid: constraint line must contain two integers l and r"
                try:
                    l = int(cparts[0])
                    r = int(cparts[1])
                except ValueError:
                    return "invalid: l or r is not an integer"
                if not (1 <= l < r <= n):
                    return "invalid: must satisfy 1 <= l < r <= n"
                idx += 1
        
        if idx != len(lines):
            return "invalid: extra lines in input"
        
        return "valid"
    except Exception as e:
        return "invalid: " + str(e)
