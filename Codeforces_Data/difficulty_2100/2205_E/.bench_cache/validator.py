def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return 'invalid: empty input'
        idx = 0
        t_parts = lines[idx].split()
        if len(t_parts) != 1:
            return 'invalid: first line must contain single integer t'
        try:
            t = int(t_parts[0])
        except ValueError:
            return 'invalid: t is not an integer'
        if t < 1 or t > 8000:
            return 'invalid: t out of range [1, 8000]'
        idx += 1
        total_n = 0
        for tc in range(t):
            if idx >= len(lines):
                return 'invalid: missing n line for test case'
            n_parts = lines[idx].split()
            if len(n_parts) != 1:
                return 'invalid: n line must contain a single integer'
            try:
                n = int(n_parts[0])
            except ValueError:
                return 'invalid: n is not an integer'
            if n < 1 or n > 8000:
                return 'invalid: n out of range [1, 8000]'
            idx += 1
            total_n += n
            if total_n > 8000:
                return 'invalid: sum of n over all test cases exceeds 8000'
            if idx >= len(lines):
                return 'invalid: missing array line for test case'
            arr_parts = lines[idx].split()
            if len(arr_parts) != n:
                return 'invalid: array length does not match n'
            for x in arr_parts:
                try:
                    v = int(x)
                except ValueError:
                    return 'invalid: array element is not an integer'
                if v < 1 or v > 8000:
                    return 'invalid: array element out of range [1, 8000]'
            idx += 1
        if idx != len(lines):
            return 'invalid: extra lines after test cases'
        return 'valid'
    except Exception as e:
        return 'invalid: ' + str(e)
