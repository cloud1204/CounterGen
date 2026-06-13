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
            return "invalid: first line must contain a single integer t"
        try:
            t = int(first[0])
        except ValueError:
            return "invalid: t is not an integer"
        if t < 1 or t > 1000:
            return "invalid: t must satisfy 1 <= t <= 1000"
        idx += 1
        total_m = 0
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case data"
            header = lines[idx].split()
            idx += 1
            if len(header) != 2:
                return "invalid: each test case header must contain two integers n and m"
            try:
                n = int(header[0])
                m = int(header[1])
            except ValueError:
                return "invalid: n or m is not an integer"
            if not (2 <= n <= m <= 3000):
                return "invalid: must satisfy 2 <= n <= m <= 3000"
            total_m += m
            if total_m > 3000:
                return "invalid: sum of m over all test cases exceeds 3000"
            if idx >= len(lines):
                return "invalid: missing sequence line"
            arr = lines[idx].split()
            idx += 1
            if len(arr) != n:
                return "invalid: sequence length does not match n"
            for x in arr:
                try:
                    v = int(x)
                except ValueError:
                    return "invalid: sequence element is not an integer"
                if v < 0 or v > m:
                    return "invalid: sequence element must be in [0, m]"
        if idx != len(lines):
            return "invalid: extra data after test cases"
        return "valid"
    except Exception as e:
        return f"invalid: {e}"
