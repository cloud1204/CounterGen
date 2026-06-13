def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return "invalid: empty input"
        
        idx = 0
        first = lines[idx].split()
        if len(first) != 1:
            return "invalid: first line must contain single integer T"
        try:
            T = int(first[0])
        except:
            return "invalid: T is not an integer"
        if T < 1 or T > 10**4:
            return "invalid: T must be in [1, 10^4]"
        idx += 1
        
        total_n = 0
        total_m = 0
        
        from collections import defaultdict
        
        for tc in range(T):
            if idx >= len(lines):
                return "invalid: not enough lines for test cases"
            header = lines[idx].split()
            if len(header) != 2:
                return "invalid: test case header must have two integers n and m"
            try:
                n, m = int(header[0]), int(header[1])
            except:
                return "invalid: n or m is not an integer"
            if n < 1 or n > 10**6:
                return "invalid: n must be in [1, 10^6]"
            if m < 0 or m > 10**6:
                return "invalid: m must be in [0, 10^6]"
            total_n += n
            total_m += m
            if total_n > 10**6:
                return "invalid: sum of n exceeds 10^6"
            if total_m > 10**6:
                return "invalid: sum of m exceeds 10^6"
            idx += 1
            
            parent = list(range(n + 1))
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            
            edge_count = 0
            for i in range(m):
                if idx >= len(lines):
                    return "invalid: not enough edge lines"
                parts = lines[idx].split()
                if len(parts) != 3:
                    return "invalid: edge line must have three integers u, v, w"
                try:
                    u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                except:
                    return "invalid: edge values not integers"
                if u < 1 or u > n:
                    return "invalid: u must be in [1, n]"
                if v < 1 or v > n:
                    return "invalid: v must be in [1, n]"
                if w < 1 or w > 10**9:
                    return "invalid: w must be in [1, 10^9]"
                ru, rv = find(u), find(v)
                if ru != rv:
                    parent[ru] = rv
                    edge_count += 1
                idx += 1
            
            root = find(1)
            for v in range(1, n + 1):
                if find(v) != root:
                    return "invalid: graph is not connected"
        
        if idx != len(lines):
            return "invalid: extra lines after test cases"
        
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
