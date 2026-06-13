def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        if len(lines) > 0 and lines[-1] == '':
            lines = lines[:-1]
        if len(lines) < 1:
            return "invalid: empty input"
        first = lines[0]
        if first != first.strip():
            return "invalid: leading/trailing whitespace in first line"
        try:
            t = int(first)
        except ValueError:
            return "invalid: first line is not an integer"
        if str(t) != first:
            return "invalid: first line not canonical integer"
        if t < 1 or t > 1000:
            return "invalid: t out of range [1, 1000]"
        if len(lines) - 1 != t:
            return f"invalid: expected {t} test cases, got {len(lines) - 1}"
        total = 0
        for i in range(1, t + 1):
            line = lines[i]
            if line != line.strip():
                return f"invalid: leading/trailing whitespace in test case line {i}"
            try:
                n = int(line)
            except ValueError:
                return f"invalid: test case {i} is not an integer"
            if str(n) != line:
                return f"invalid: test case {i} not canonical integer"
            if n < 1 or n > 10**12:
                return f"invalid: n out of range [1, 10^12] in test case {i}"
            total += n
        if total > 10**12:
            return "invalid: sum of n exceeds 10^12"
        return "valid"
    except Exception as e:
        return f"invalid: {str(e)}"
