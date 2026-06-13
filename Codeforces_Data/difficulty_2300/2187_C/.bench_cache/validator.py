def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return "invalid: empty input"
        
        idx = 0
        first_line = lines[idx].split()
        if len(first_line) != 1:
            return "invalid: first line must contain single integer t"
        try:
            t = int(first_line[0])
        except ValueError:
            return "invalid: t is not an integer"
        if t < 1 or t > 10**4:
            return "invalid: t must satisfy 1 <= t <= 10^4"
        idx += 1
        
        total_n = 0
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case data"
            nm_parts = lines[idx].split()
            if len(nm_parts) != 2:
                return "invalid: test case header must contain n and m"
            try:
                n, m = int(nm_parts[0]), int(nm_parts[1])
            except ValueError:
                return "invalid: n or m is not an integer"
            if n < 2 or n > 2 * 10**5:
                return "invalid: n must satisfy 2 <= n <= 2*10^5"
            if m < 0 or m > n - 2:
                return "invalid: m must satisfy 0 <= m <= n-2"
            total_n += n
            if total_n > 2 * 10**5:
                return "invalid: sum of n over all test cases exceeds 2*10^5"
            idx += 1
            
            edges = []
            edge_set = set()
            for i in range(m):
                if idx >= len(lines):
                    return "invalid: missing edge data"
                uv_parts = lines[idx].split()
                if len(uv_parts) != 2:
                    return "invalid: edge line must contain u and v"
                try:
                    u, v = int(uv_parts[0]), int(uv_parts[1])
                except ValueError:
                    return "invalid: u or v is not an integer"
                if u < 1 or u > n or v < 1 or v > n:
                    return "invalid: u and v must satisfy 1 <= u,v <= n"
                if u + 1 >= v:
                    return "invalid: extra edge must satisfy u+1 < v"
                if (u, v) in edge_set:
                    return "invalid: duplicate edge"
                edge_set.add((u, v))
                edges.append((u, v))
                idx += 1
            
            for i in range(len(edges)):
                for j in range(len(edges)):
                    if i == j:
                        continue
                    ui, vi = edges[i]
                    uj, vj = edges[j]
                    if ui < uj < vi < vj:
                        return "invalid: forbidden crossing edges exist"
        
        if idx != len(lines):
            return "invalid: extra lines in input"
        
        return "valid"
    except Exception as e:
        return f"invalid: parsing error {str(e)}"
