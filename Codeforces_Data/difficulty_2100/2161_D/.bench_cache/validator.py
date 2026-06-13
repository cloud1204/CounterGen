def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        if lines and lines[-1] == '':
            lines = lines[:-1]
        if len(lines) == 0:
            return "invalid: empty input"
        
        idx = 0
        t_line = lines[idx].split()
        if len(t_line) != 1:
            return "invalid: first line must contain single integer t"
        try:
            t = int(t_line[0])
        except:
            return "invalid: t is not an integer"
        if t < 1 or t > 6 * 10**4:
            return "invalid: t out of range [1, 6*10^4]"
        idx += 1
        
        total_n = 0
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case data"
            n_line = lines[idx].split()
            if len(n_line) != 1:
                return "invalid: n line must contain single integer"
            try:
                n = int(n_line[0])
            except:
                return "invalid: n is not an integer"
            if n < 1 or n > 3 * 10**5:
                return "invalid: n out of range [1, 3*10^5]"
            idx += 1
            total_n += n
            if total_n > 3 * 10**5:
                return "invalid: sum of n over all test cases exceeds 3*10^5"
            
            if idx >= len(lines):
                return "invalid: missing array line"
            a_line = lines[idx].split()
            if len(a_line) != n:
                return "invalid: array length does not match n"
            try:
                a = [int(x) for x in a_line]
            except:
                return "invalid: array contains non-integer"
            for x in a:
                if x < 1 or x > n:
                    return "invalid: array element out of range [1, n]"
            idx += 1
        
        if idx != len(lines):
            return "invalid: extra lines in input"
        
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
