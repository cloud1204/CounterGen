def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if len(lines) < 2:
            return "invalid: not enough lines"
        
        first_line = lines[0].split()
        if len(first_line) != 2:
            return "invalid: first line must contain exactly 2 integers"
        try:
            n = int(first_line[0])
            m = int(first_line[1])
        except ValueError:
            return "invalid: n and m must be integers"
        
        if not (1 <= n <= 500):
            return "invalid: n must satisfy 1 <= n <= 500"
        if not (1 <= m <= 500):
            return "invalid: m must satisfy 1 <= m <= 500"
        
        second_line = lines[1].split()
        if len(second_line) != n:
            return "invalid: second line must contain exactly n integers"
        
        try:
            c = [int(x) for x in second_line]
        except ValueError:
            return "invalid: strengths must be integers"
        
        for ci in c:
            if not (0 <= ci <= 60):
                return "invalid: each c_i must satisfy 0 <= c_i <= 60"
        
        if len(lines) < 2 + m:
            return "invalid: not enough query lines"
        if len(lines) > 2 + m:
            return "invalid: too many lines"
        
        herd = {}
        for ci in c:
            herd[ci] = herd.get(ci, 0) + 1
        
        for i in range(m):
            query_line = lines[2 + i].split()
            if len(query_line) != 2:
                return f"invalid: query {i+1} must contain exactly 2 integers"
            try:
                t = int(query_line[0])
                x = int(query_line[1])
            except ValueError:
                return f"invalid: query {i+1} values must be integers"
            
            if t not in (1, 2, 3):
                return f"invalid: query type must be 1, 2, or 3"
            
            if t == 1:
                if not (0 <= x <= 60):
                    return f"invalid: query 1 x must satisfy 0 <= x <= 60"
                herd[x] = herd.get(x, 0) + 1
            elif t == 2:
                if not (0 <= x <= 60):
                    return f"invalid: query 2 x must satisfy 0 <= x <= 60"
                if herd.get(x, 0) < 1:
                    return f"invalid: query 2 attempts to remove non-existent reindeer with strength 2^{x}"
                herd[x] -= 1
            else:
                if not (1 <= x <= 10**18):
                    return f"invalid: query 3 x must satisfy 1 <= x <= 10^18"
        
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
