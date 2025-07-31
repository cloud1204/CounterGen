def normalize_lines(text):
    # strip trailing spaces, remove trailing empty lines
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and lines[-1] == '':
        lines.pop()
    # Normalize YES/NO into lowercase (common feature in Codeforces problems)
    normalized = []
    for line in lines:
        if line.strip().lower() in ('yes', 'no'):
            normalized.append(line.strip().lower())
        else:
            normalized.append(line)
    return normalized
def check_match(outputA, outputB):
    lines1 = normalize_lines(outputA)
    lines2 = normalize_lines(outputB)
    return lines1 == lines2