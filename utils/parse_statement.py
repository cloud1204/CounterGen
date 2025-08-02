import re
def parse_statement(text: str) -> str:
    pattern = r"standard output</div></div>(.*?)<div class=\"sample-tests\">"

    matches = re.findall(pattern, text, re.DOTALL)
    if len(matches) == 1:
        return matches[0]
    else:
        return text
