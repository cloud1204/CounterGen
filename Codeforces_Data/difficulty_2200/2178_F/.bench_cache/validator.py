def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return "invalid: empty input"
        
        idx = 0
        try:
            t = int(lines[idx])
        except ValueError:
            return "invalid: t is not an integer"
        idx += 1
        
        if t < 1 or t > 10**4:
            return "invalid: t out of range [1, 10^4]"
        
        total_n = 0
        
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing n for test case"
            try:
                n = int(lines[idx])
            except ValueError:
                return "invalid: n is not an integer"
            idx += 1
            
            if n < 2 or n > 2 * 10**5:
                return "invalid: n out of range [2, 2*10^5]"
            
            total_n += n
            if total_n > 2 * 10**5:
                return "invalid: sum of n exceeds 2*10^5"
            
            parent = list(range(n + 1))
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            
            edges_seen = set()
            
            for i in range(n - 1):
                if idx >= len(lines):
                    return "invalid: missing edge line"
                parts = lines[idx].split()
                idx += 1
                if len(parts) != 2:
                    return "invalid: edge line does not have exactly 2 integers"
                try:
                    u, v = int(parts[0]), int(parts[1])
                except ValueError:
                    return "invalid: edge contains non-integer"
                
                if not (1 <= u < v <= n):
                    return "invalid: edge constraint 1 <= u_i < v_i <= n violated"
                
                if (u, v) in edges_seen:
                    return "invalid: duplicate edge"
                edges_seen.add((u, v))
                
                ru, rv = find(u), find(v)
                if ru == rv:
                    return "invalid: edges do not form a tree (cycle)"
                parent[ru] = rv
            
            root = find(1)
            for v in range(2, n + 1):
                if find(v) != root:
                    return "invalid: edges do not form a tree (disconnected)"
        
        if idx != len(lines):
            return "invalid: extra lines at end of input"
        
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
