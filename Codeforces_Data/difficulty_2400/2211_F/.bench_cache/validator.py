def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return 'invalid: empty input'
        try:
            t = int(lines[0])
        except ValueError:
            return 'invalid: first line is not an integer'
        if lines[0] != str(t):
            return 'invalid: first line has extra characters'
        if t < 1 or t > 10**4:
            return 'invalid: t out of range (1 <= t <= 10^4)'
        if len(lines) - 1 != t:
            return 'invalid: number of test case lines does not match t'
        sum_n = 0
        sum_m = 0
        for i in range(1, t + 1):
            parts = lines[i].split()
            if len(parts) != 2:
                return f'invalid: test case {i} does not contain exactly 2 integers'
            try:
                n = int(parts[0])
                m = int(parts[1])
            except ValueError:
                return f'invalid: test case {i} contains non-integer values'
            if parts[0] != str(n) or parts[1] != str(m):
                return f'invalid: test case {i} has malformed integers'
            if n < 3 or n > 10**6:
                return f'invalid: test case {i} n out of range (3 <= n <= 10^6)'
            if m < 3 or m > 10**6:
                return f'invalid: test case {i} m out of range (3 <= m <= 10^6)'
            sum_n += n
            sum_m += m
        if sum_n > 10**6:
            return 'invalid: sum of n exceeds 10^6'
        if sum_m > 10**6:
            return 'invalid: sum of m exceeds 10^6'
        return 'valid'
    except Exception as e:
        return f'invalid: {str(e)}'
