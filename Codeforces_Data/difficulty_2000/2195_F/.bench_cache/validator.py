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
            return "invalid: first line must contain single integer t"
        try:
            t = int(first[0])
        except ValueError:
            return "invalid: t is not an integer"
        if t < 1 or t > 10**4:
            return "invalid: t out of range (1 <= t <= 10^4)"
        idx += 1
        total_n_squared = 0
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case data"
            n_parts = lines[idx].split()
            if len(n_parts) != 1:
                return "invalid: n line must contain single integer"
            try:
                n = int(n_parts[0])
            except ValueError:
                return "invalid: n is not an integer"
            if n < 1 or n > 3000:
                return "invalid: n out of range (1 <= n <= 3000)"
            idx += 1
            total_n_squared += n * n
            if total_n_squared > 3000 * 3000:
                return "invalid: sum of n^2 exceeds 3000^2"
            funcs = set()
            for i in range(n):
                if idx >= len(lines):
                    return "invalid: missing function line"
                parts = lines[idx].split()
                if len(parts) != 3:
                    return "invalid: function line must contain three integers"
                try:
                    a, b, c = int(parts[0]), int(parts[1]), int(parts[2])
                except ValueError:
                    return "invalid: function coefficients not integers"
                if a < -10**6 or a > 10**6:
                    return "invalid: a out of range"
                if b < -10**6 or b > 10**6:
                    return "invalid: b out of range"
                if c < -10**6 or c > 10**6:
                    return "invalid: c out of range"
                if a == 0:
                    return "invalid: a must be non-zero"
                if (a, b, c) in funcs:
                    return "invalid: functions in a test case must be pairwise distinct"
                funcs.add((a, b, c))
                idx += 1
        if idx != len(lines):
            return "invalid: extra lines at end of input"
        return "valid"
    except Exception as e:
        return f"invalid: parsing error {e}"
