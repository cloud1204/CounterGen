def normalize_lines(text):
    # Strip trailing spaces, keep exact 1 trailing empty lines
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and lines[-1] == '':
        lines.pop()
    lines.append('')
    # Normalize YES/NO into lowercase (common feature in Codeforces problems)
    normalized = []
    for line in lines:
        if line.strip().lower() in ('yes', 'no'):
            normalized.append(line.strip().lower())
        else:
            normalized.append(line)
    return "\n".join(normalized)
def check_match(outputA, outputB):
    lines1 = normalize_lines(outputA)
    lines2 = normalize_lines(outputB)
    if lines1 != lines2:
        return f"expected:\n{str(lines2)}\nfound:\n{str(lines1)}"
    return "AC"