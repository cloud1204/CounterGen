def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        
        idx = 0
        if idx >= len(lines):
            return "invalid: missing t"
        
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
                return f"invalid: missing n for test case {tc+1}"
            
            try:
                n = int(lines[idx])
            except ValueError:
                return f"invalid: n is not an integer for test case {tc+1}"
            idx += 1
            
            if n < 1 or n > 2 * 10**5:
                return f"invalid: n out of range [1, 2*10^5] for test case {tc+1}"
            
            total_n += n
            if total_n > 2 * 10**5:
                return "invalid: sum of n exceeds 2*10^5"
            
            if idx >= len(lines):
                return f"invalid: missing array a for test case {tc+1}"
            
            a_parts = lines[idx].split()
            idx += 1
            
            if len(a_parts) != n:
                return f"invalid: array a does not have n elements for test case {tc+1}"
            
            for x in a_parts:
                try:
                    val = int(x)
                except ValueError:
                    return f"invalid: a value is not an integer for test case {tc+1}"
                if val < 1 or val > 10**9:
                    return f"invalid: a value out of range [1, 10^9] for test case {tc+1}"
            
            parent = list(range(n + 1))
            
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x
            
            edge_count = 0
            for e in range(n - 1):
                if idx >= len(lines):
                    return f"invalid: missing edge for test case {tc+1}"
                
                edge_parts = lines[idx].split()
                idx += 1
                
                if len(edge_parts) != 2:
                    return f"invalid: edge does not have 2 vertices for test case {tc+1}"
                
                try:
                    v = int(edge_parts[0])
                    u = int(edge_parts[1])
                except ValueError:
                    return f"invalid: edge vertices not integers for test case {tc+1}"
                
                if v < 1 or v > n or u < 1 or u > n:
                    return f"invalid: edge vertex out of range [1, n] for test case {tc+1}"
                
                if v == u:
                    return f"invalid: self loop edge for test case {tc+1}"
                
                rv = find(v)
                ru = find(u)
                if rv == ru:
                    return f"invalid: cycle detected (not a tree) for test case {tc+1}"
                parent[rv] = ru
                edge_count += 1
            
            if n >= 1 and edge_count != n - 1:
                return f"invalid: wrong number of edges for test case {tc+1}"
        
        if idx != len(lines):
            return "invalid: extra lines at end"
        
        return "valid"
    except Exception as e:
        return f"invalid: parsing error {str(e)}"
