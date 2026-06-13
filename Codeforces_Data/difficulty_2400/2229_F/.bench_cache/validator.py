def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        while lines and lines[-1] == '':
            lines.pop()
        if not lines:
            return "invalid: empty input"
        try:
            t = int(lines[0])
        except:
            return "invalid: t is not an integer"
        if t < 1 or t > 10**4:
            return "invalid: t must be 1 <= t <= 10^4"
        idx = 1
        total_2n = 0
        for tc in range(t):
            if idx >= len(lines):
                return "invalid: missing test case lines"
            first = lines[idx].split()
            idx += 1
            if len(first) != 2:
                return "invalid: first line of test case must have two integers n and k"
            try:
                n, k = int(first[0]), int(first[1])
            except:
                return "invalid: n and k must be integers"
            if not (1 <= k <= n <= 18):
                return "invalid: must satisfy 1 <= k <= n <= 18"
            if idx >= len(lines):
                return "invalid: missing array line"
            arr = lines[idx].split()
            idx += 1
            if len(arr) != n:
                return "invalid: array must contain exactly n integers"
            try:
                arr = [int(x) for x in arr]
            except:
                return "invalid: array elements must be integers"
            for x in arr:
                if x < 1 or x > 10**9:
                    return "invalid: must satisfy 1 <= a_i <= 10^9"
            total_2n += 2**n
            if total_2n > 2**18:
                return "invalid: sum of 2^n exceeds 2^18"
        if idx != len(lines):
            return "invalid: extra lines after test cases"
        return "valid"
    except Exception as e:
        return "invalid: " + str(e)
