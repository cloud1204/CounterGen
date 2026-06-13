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
            return "invalid: t is not an integer"
        
        if t < 1 or t > 10**4:
            return "invalid: t out of range [1, 10^4]"
        
        idx = 1
        total_n = 0
        
        for tc in range(t):
            if idx >= len(lines):
                return f"invalid: missing n for test case {tc+1}"
            
            try:
                n = int(lines[idx])
            except ValueError:
                return f"invalid: n is not an integer for test case {tc+1}"
            
            if n < 2 or n > 300000:
                return f"invalid: n out of range [2, 300000] for test case {tc+1}"
            
            if n % 2 != 0:
                return f"invalid: n is not even for test case {tc+1}"
            
            idx += 1
            
            if idx >= len(lines):
                return f"invalid: missing string S for test case {tc+1}"
            
            S = lines[idx]
            idx += 1
            
            if len(S) != n:
                return f"invalid: length of S does not match n for test case {tc+1}"
            
            for ch in S:
                if ch != '(' and ch != ')':
                    return f"invalid: S contains invalid character for test case {tc+1}"
            
            balance = 0
            for ch in S:
                if ch == '(':
                    balance += 1
                else:
                    balance -= 1
                if balance < 0:
                    return f"invalid: S is not a regular bracket sequence for test case {tc+1}"
            
            if balance != 0:
                return f"invalid: S is not a regular bracket sequence for test case {tc+1}"
            
            total_n += n
            
            if total_n > 300000:
                return "invalid: sum of n over all test cases exceeds 300000"
        
        if idx != len(lines):
            return "invalid: extra lines in input"
        
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
