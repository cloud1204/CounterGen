import re

def extract_between(text, a, b):
    pattern = rf"{re.escape(a)}(.*?){re.escape(b)}"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None
def parse_codeforces(text: str) -> str:
    problem_statement = extract_between(text, "standard output</div></div>" , "<div class=\"sample-tests\">")
    return problem_statement, None, None

def parse_atcoder(text : str) -> tuple[str, str, str]:
    lines = text.splitlines()
    statement_start = False
    problem_statement = ''
    for line in lines:
        if '<h3>Problem Statement</h3>' in line:
            statement_start = True
        if statement_start:
            problem_statement += line
        if '<h3>Output</h3>' in line:
            statement_start = False
    example_input = extract_between(text, "<h3>Sample Input 1</h3><pre>", "</pre>")
    example_input = example_input.replace("\r", "")
    example_output = extract_between(text, "<h3>Sample Output 1</h3><pre>", "</pre>")
    example_output = example_output.replace("\r", "")
    return problem_statement, example_input, example_output

def parse_cses(text: str):
    problem_statement = extract_between(text, "<div class=\"md\"><p>", "<h1 id=\"example\">Example</h1>")
    example_input = extract_between(text, "<p>Input:</p>\n<pre>", "</pre>")
    example_output = extract_between(text, "<p>Output:</p>\n<pre>", "</pre>")
    return problem_statement, example_input, example_output

def parse_statement(text_or_url: str):
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0"  # Some websites block default Python user agents
    }

    if 'https' == text_or_url[:5]:
        if 'atcoder' in text_or_url:
            text = requests.get(text_or_url, headers=headers).text
            return parse_atcoder(text)
        elif 'cses' in text_or_url:
            text = requests.get(text_or_url, headers=headers).text
            return parse_cses(text)
        else:
            raise ValueError("Unsupported URL.")
    else:
        if 'codeforces' in text_or_url or 'Codeforces' in text_or_url:
            return parse_codeforces(text_or_url)
        if 'AtCoder Inc.' in text_or_url:
            return parse_atcoder(text_or_url)
        elif 'CSES Problem Set' in text_or_url:
            return parse_cses(text_or_url)
        return text_or_url, None, None # Fallback: assume user pastes the statement/Input/output itself


if __name__ == '__main__':
    print(parse_statement("https://cses.fi/problemset/task/2422"))