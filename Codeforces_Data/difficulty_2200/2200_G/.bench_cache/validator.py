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
        except:
            return 'invalid: t is not an integer'
        idx += 1
        
        if not (1 <= t <= 1000):
            return 'invalid: 1 <= t <= 1000 violated'
        
        total_n_squared = 0
        
        for tc in range(t):
            if idx >= len(lines):
                return 'invalid: missing test case line'
            first_line = lines[idx].split()
            idx += 1
            if len(first_line) != 2:
                return 'invalid: first line of testcase must contain n and x'
            try:
                n = int(first_line[0])
                x = int(first_line[1])
            except:
                return 'invalid: n or x not integer'
            
            if not (1 <= n <= 3000):
                return 'invalid: 1 <= n <= 3000 violated'
            if not (1 <= x <= 10**9):
                return 'invalid: 1 <= x <= 10^9 violated'
            
            total_n_squared += n * n
            if total_n_squared > 3000 * 3000:
                return 'invalid: sum of n^2 over all test cases exceeds 3000^2'
            
            if idx >= len(lines):
                return 'invalid: missing operations line'
            ops = lines[idx].split()
            idx += 1
            
            if len(ops) != n:
                return 'invalid: number of operations does not match n'
            
            for op in ops:
                if len(op) < 2:
                    return 'invalid: operation too short'
                if op[0] not in '+-x/':
                    return 'invalid: operation must start with +, -, x, or /'
                try:
                    y = int(op[1:])
                except:
                    return 'invalid: operation operand not an integer'
                if not (1 <= y <= 10**9):
                    return 'invalid: 1 <= y <= 10^9 violated'
                if op[1:] != str(y):
                    return 'invalid: operand has invalid format'
        
        if idx != len(lines):
            return 'invalid: extra lines in input'
        
        return 'valid'
    except Exception as e:
        return 'invalid: ' + str(e)
