def validate(full_testcase: str) -> str:
    try:
        lines = full_testcase.split('\n')
        if len(lines) < 2:
            return 'invalid: must have at least 2 lines'
        
        first_line = lines[0].split()
        if len(first_line) != 3:
            return 'invalid: first line must contain exactly 3 integers'
        
        try:
            n = int(first_line[0])
            m = int(first_line[1])
            k = int(first_line[2])
        except ValueError:
            return 'invalid: n, m, k must be integers'
        
        if not (1 <= n <= 3000):
            return 'invalid: 1 <= n <= 3000 violated'
        if not (0 <= m <= 3000):
            return 'invalid: 0 <= m <= 3000 violated'
        if not (1 <= k <= n):
            return 'invalid: 1 <= k <= n violated'
        
        rope = lines[1]
        if len(rope) != n:
            return 'invalid: rope length must equal n'
        
        for ch in rope:
            if ch not in ('R', 'B'):
                return 'invalid: rope must contain only R and B characters'
        
        return 'valid'
    except Exception as e:
        return f'invalid: {str(e)}'
