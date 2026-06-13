def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        if len(lines) > 0 and lines[-1] == '':
            lines = lines[:-1]
        
        if len(lines) == 0:
            return "invalid: empty input"
        
        try:
            t = int(lines[0])
        except ValueError:
            return "invalid: first line is not an integer"
        
        if t < 1 or t > 10**4:
            return "invalid: t must satisfy 1 <= t <= 10^4"
        
        idx = 1
        total_n = 0
        
        for tc in range(t):
            if idx >= len(lines):
                return f"invalid: missing line for n in test case {tc+1}"
            
            try:
                n = int(lines[idx])
            except ValueError:
                return f"invalid: n in test case {tc+1} is not an integer"
            
            if n < 1 or n > 2 * 10**5:
                return f"invalid: n must satisfy 1 <= n <= 2*10^5 in test case {tc+1}"
            
            total_n += n
            if total_n > 2 * 10**5:
                return "invalid: sum of n over all test cases exceeds 2*10^5"
            
            idx += 1
            
            if idx >= len(lines):
                return f"invalid: missing array line in test case {tc+1}"
            
            parts = lines[idx].split()
            if len(parts) != n:
                return f"invalid: array length does not match n in test case {tc+1}"
            
            for p in parts:
                try:
                    val = int(p)
                except ValueError:
                    return f"invalid: array element is not an integer in test case {tc+1}"
                if val < 0 or val > 10**9:
                    return f"invalid: array element must satisfy 0 <= a_i <= 10^9 in test case {tc+1}"
            
            idx += 1
        
        if idx != len(lines):
            return "invalid: extra lines in input"
        
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
