def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return 'invalid: empty input'
        
        idx = 0
        try:
            t = int(lines[idx])
        except ValueError:
            return 'invalid: t is not an integer'
        idx += 1
        
        if t < 1 or t > 10**4:
            return 'invalid: t out of range [1, 10^4]'
        
        total_n = 0
        for tc in range(t):
            if idx >= len(lines):
                return 'invalid: missing line for n'
            try:
                n = int(lines[idx])
            except ValueError:
                return 'invalid: n is not an integer'
            idx += 1
            
            if n < 1 or n > 2 * 10**5:
                return 'invalid: n out of range [1, 2*10^5]'
            
            total_n += n
            if total_n > 2 * 10**5:
                return 'invalid: sum of n exceeds 2*10^5'
            
            if idx >= len(lines):
                return 'invalid: missing line for v'
            try:
                v = list(map(int, lines[idx].split()))
            except ValueError:
                return 'invalid: v contains non-integer'
            idx += 1
            
            if len(v) != n:
                return 'invalid: v length does not match n'
            
            for vi in v:
                if vi < -10**9 or vi > 10**9:
                    return 'invalid: v_i out of range [-10^9, 10^9]'
            
            if idx >= len(lines):
                return 'invalid: missing line for a'
            try:
                a = list(map(int, lines[idx].split()))
            except ValueError:
                return 'invalid: a contains non-integer'
            idx += 1
            
            if len(a) != n:
                return 'invalid: a length does not match n'
            
            for ai in a:
                if ai < 1 or ai > n:
                    return 'invalid: a_i out of range [1, n]'
            
            if len(set(a)) != n:
                return 'invalid: a contains duplicates'
            
            if idx >= len(lines):
                return 'invalid: missing line for b'
            try:
                b = list(map(int, lines[idx].split()))
            except ValueError:
                return 'invalid: b contains non-integer'
            idx += 1
            
            if len(b) != n:
                return 'invalid: b length does not match n'
            
            for bi in b:
                if bi < 1 or bi > n:
                    return 'invalid: b_i out of range [1, n]'
            
            if len(set(b)) != n:
                return 'invalid: b contains duplicates'
        
        if idx != len(lines):
            return 'invalid: extra lines at end'
        
        return 'valid'
    except Exception as e:
        return 'invalid: ' + str(e)
