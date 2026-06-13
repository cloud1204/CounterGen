"""
Set up a new problem folder for data collection.

For a folder containing statement.txt (raw Codeforces HTML), this script:
  - Parses it into statement.md
  - Creates AC.txt and WA1.txt through WA5.txt (empty)

Usage:
  python setup_problem.py <problem_id>

Example:
  python setup_problem.py 2201_C
"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ROOT)
from CF_parser.parser import codeforces_html_to_markdown

DATA_DIR = os.path.join(_ROOT, "Codeforces_Data")


def find_folder(problem_id: str) -> str:
    for dirpath, dirnames, _ in os.walk(DATA_DIR):
        if problem_id in dirnames:
            return os.path.join(dirpath, problem_id)
    return None


def setup_problem(problem_id: str):
    folder = find_folder(problem_id)
    if folder is None:
        print(f"Error: no folder named '{problem_id}' found under {DATA_DIR}")
        sys.exit(1)

    statement_txt = os.path.join(folder, "statement.txt")
    if not os.path.exists(statement_txt):
        print(f"Error: {statement_txt} not found.")
        sys.exit(1)

    with open(statement_txt, "r", encoding="utf-8") as f:
        html = f.read()

    md = codeforces_html_to_markdown(html)
    md_path = os.path.join(folder, "statement.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Written: {md_path}")
    os.remove(statement_txt)
    print(f"Deleted: {statement_txt}")

    for name in ["AC.txt"] + [f"WA{i}.txt" for i in range(1, 6)]:
        path = os.path.join(folder, name)
        if not os.path.exists(path):
            open(path, "w").close()
            print(f"Created: {path}")
        else:
            print(f"Skipped (exists): {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    setup_problem(sys.argv[1].strip("/\\"))
