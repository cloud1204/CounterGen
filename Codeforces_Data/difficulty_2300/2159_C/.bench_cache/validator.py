def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return "invalid: empty input"
        idx = 0
        t_parts = lines[idx].split()
        if len(t_parts) != 1:
            return "invalid: first line must contain single integer t"
        try:
            t = int(t_parts[0])
        except:
            return "invalid: t is not an integer"
        if t < 1 or t > 10**4:
            return "invalid: t out of range 1 <= t <= 10^4"
        idx += 1
        total_n = 0
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case data"
            n_parts = lines[idx].split()
            if len(n_parts) != 1:
                return "invalid: n line must contain single integer"
            try:
                n = int(n_parts[0])
            except:
                return "invalid: n is not an integer"
            if n < 1 or n > 4 * 10**5:
                return "invalid: n out of range 1 <= n <= 4*10^5"
            total_n += n
            if total_n > 4 * 10**5:
                return "invalid: sum of n exceeds 4*10^5"
            idx += 1
            if idx >= len(lines):
                return "invalid: missing coefficients line"
            a_parts = lines[idx].split()
            if len(a_parts) != n + 1:
                return "invalid: number of coefficients does not match n+1"
            try:
                a = [int(x) for x in a_parts]
            except:
                return "invalid: coefficient is not an integer"
            for v in a:
                if v < -1 or v > 10**9:
                    return "invalid: coefficient out of range -1 <= a_i <= 10^9"
            if a[0] != -1:
                return "invalid: a_0 must be -1"
            if a[n] != -1:
                return "invalid: a_n must be -1"
            idx += 1
        if idx != len(lines):
            return "invalid: extra lines in input"
        return "valid"
    except Exception as e:
        return "invalid: " + str(e)
