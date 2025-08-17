import re

def _find_matching(src: str, open_pos: int, open_ch: str, close_ch: str) -> int:
    """Return index of matching close_ch for the open_ch at open_pos; -1 if not found.
       Skips //... , /*...*/ , '...' , "..." , and raw strings R"delim(... )delim"."""
    n = len(src)
    i = open_pos
    if i < 0 or i >= n or src[i] != open_ch:
        return -1

    depth = 0
    in_sl = in_ml = in_sq = in_dq = in_raw = False
    raw_end = ""
    esc = False

    while i < n:
        c = src[i]

        # line comment
        if in_sl:
            if c == '\n':
                in_sl = False
            i += 1
            continue

        # block comment
        if in_ml:
            if c == '*' and i+1 < n and src[i+1] == '/':
                in_ml = False
                i += 2
            else:
                i += 1
            continue

        # raw string
        if in_raw:
            if src.startswith(raw_end, i):
                in_raw = False
                i += len(raw_end)
            else:
                i += 1
            continue

        # single-quoted
        if in_sq:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == "'":
                in_sq = False
            i += 1
            continue

        # double-quoted
        if in_dq:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_dq = False
            i += 1
            continue

        # tokens outside of strings/comments
        if c == '/' and i+1 < n:
            if src[i+1] == '/':
                in_sl = True; i += 2; continue
            if src[i+1] == '*':
                in_ml = True; i += 2; continue

        if c == 'R' and i+1 < n and src[i+1] == '"':
            # R"delim(... )delim"
            j = i+2
            while j < n and src[j] != '(':
                j += 1
            delim = src[i+2:j] if j < n else ""
            raw_end = ')' + delim + '"'
            in_raw = True
            i = j+1
            continue

        if c == "'":
            in_sq = True; i += 1; continue
        if c == '"':
            in_dq = True; i += 1; continue

        # brace/paren tracking
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1

    return -1

def _skip_ws_comments(src: str, i: int) -> int:
    n = len(src)
    while i < n:
        if src.startswith('//', i):
            j = src.find('\n', i)
            i = n if j == -1 else j+1
        elif src.startswith('/*', i):
            j = src.find('*/', i+2)
            i = n if j == -1 else j+2
        elif i < n and src[i] in ' \t\r\n\f\v':
            i += 1
        else:
            break
    return i

def insert_return0_in_main(code: str) -> str:
    """
    Insert 'return 0;' right before the closing '}' of user_main(...).
    If user_main's body can't be located, fall back to inserting before the LAST '}' in the file.
    If no '}' exists, return the code unchanged.
    """
    s = code

    # 1) locate identifier 'user_main'
    m = re.search(r'(?<!\w)main(?!\w)', s)
    if m:
        i = m.end()
        # find '(' after optional ws/comments
        i = _skip_ws_comments(s, i)
        if i < len(s) and s[i] == '(':
            rp = _find_matching(s, i, '(', ')')
            if rp != -1:
                # skip to the function body '{'
                j = _skip_ws_comments(s, rp+1)
                if j < len(s) and s[j] == '{':
                    close = _find_matching(s, j, '{', '}')
                    if close != -1:
                        return s[:close].rstrip() + "\n    return 0;\n" + s[close:]

    # fallback: insert before the LAST '}' in the file
    last = s.rfind('}')
    if last != -1:
        return s[:last].rstrip() + "\n    return 0;\n" + s[last:]

    return s