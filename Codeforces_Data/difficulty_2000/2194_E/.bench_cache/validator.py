def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return "invalid: empty input"
        idx = 0
        t_line = lines[idx].split()
        if len(t_line) != 1:
            return "invalid: first line must contain single integer t"
        try:
            t = int(t_line[0])
        except ValueError:
            return "invalid: t is not an integer"
        if t < 1 or t > 10**4:
            return "invalid: t must satisfy 1 <= t <= 10^4"
        idx += 1
        total_nm = 0
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case data"
            nm_line = lines[idx].split()
            if len(nm_line) != 2:
                return "invalid: n m line must contain two integers"
            try:
                n = int(nm_line[0])
                m = int(nm_line[1])
            except ValueError:
                return "invalid: n or m is not an integer"
            if n < 1 or n > 10**6:
                return "invalid: n must satisfy 1 <= n <= 10^6"
            if m < 1 or m > 10**6:
                return "invalid: m must satisfy 1 <= m <= 10^6"
            if n * m < 1 or n * m > 10**6:
                return "invalid: n*m must satisfy 1 <= n*m <= 10^6"
            total_nm += n * m
            if total_nm > 10**6:
                return "invalid: sum of n*m across test cases exceeds 10^6"
            idx += 1
            has_nonneg = False
            for i in range(n):
                if idx >= len(lines):
                    return "invalid: missing row data"
                row = lines[idx].split()
                if len(row) != m:
                    return "invalid: row does not contain exactly m integers"
                for v in row:
                    try:
                        x = int(v)
                    except ValueError:
                        return "invalid: matrix value is not an integer"
                    if x < -10**9 or x > 10**9:
                        return "invalid: a_{i,j} must satisfy -10^9 <= a_{i,j} <= 10^9"
                    if x >= 0:
                        has_nonneg = True
                idx += 1
            if not has_nonneg:
                return "invalid: at least one non-negative value required"
        if idx != len(lines):
            return "invalid: extra data after test cases"
        return "valid"
    except Exception as e:
        return "invalid: " + str(e)
