def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        if len(lines) == 0:
            return 'invalid: empty input'
        idx = 0
        try:
            t = int(lines[idx])
        except:
            return 'invalid: first line must be integer t'
        idx += 1
        if not (1 <= t <= 10**3):
            return 'invalid: t must be between 1 and 10^3'
        
        total_n = 0
        for tc in range(t):
            if idx >= len(lines):
                return 'invalid: missing test case data'
            parts = lines[idx].split()
            if len(parts) != 2:
                return 'invalid: n and q line must have two integers'
            try:
                n = int(parts[0])
                q = int(parts[1])
            except:
                return 'invalid: n and q must be integers'
            idx += 1
            if not (1 <= n <= 10**6):
                return 'invalid: n must be between 1 and 10^6'
            if not (1 <= q <= 100):
                return 'invalid: q must be between 1 and 100'
            total_n += n
            if total_n > 10**6:
                return 'invalid: sum of n exceeds 10^6'
            
            if idx >= len(lines):
                return 'invalid: missing string line'
            s = lines[idx]
            idx += 1
            if len(s) != n:
                return 'invalid: string length does not match n'
            if not all('a' <= c <= 'z' for c in s):
                return 'invalid: string must contain only lowercase English letters'
            
            for i in range(q):
                if idx >= len(lines):
                    return 'invalid: missing query line'
                qparts = lines[idx].split()
                if len(qparts) != 2:
                    return 'invalid: query must have two integers'
                try:
                    l = int(qparts[0])
                    r = int(qparts[1])
                except:
                    return 'invalid: query values must be integers'
                idx += 1
                if not (1 <= l <= r <= n):
                    return 'invalid: query must satisfy 1 <= l <= r <= n'
        
        while idx < len(lines):
            if lines[idx].strip() != '':
                return 'invalid: extra non-empty lines at end'
            idx += 1
        
        return 'valid'
    except Exception as e:
        return f'invalid: {str(e)}'
