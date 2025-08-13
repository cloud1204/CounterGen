from scripts import default_checker
from utils.code import Code, split_output
from utils.agent import Agent
import re
def has_invalid_control_chars(s):
    # Control characters: ASCII 0–31, exclude \n (10) and optionally \t (9)
    return bool(re.search(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', s))

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
    if has_invalid_control_chars(outputA):
        return "Contains invalid characters"
    lines1 = normalize_lines(outputA)
    lines2 = normalize_lines(outputB)
    if lines1 != lines2:
        return f"expected:\n{str(lines2)}\nfound:\n{str(lines1)}"
    return "AC"

class Checker:
    def __init__(self, checker_code : Code = None):
        self.checker_code = checker_code
    def check(self, Input: str, outA: str, outB: str) -> str: # suppose outB is correct
        if self.checker_code == None:
            return default_checker.check_match(outputA=outA, outputB=outB)
        else:
            if has_invalid_control_chars(outA):
                return "Contains invalid characters"
            outA = default_checker.normalize_lines(outA)
            outA = default_checker.normalize_lines(outB)
            return self.checker_code.execute(args=[Input, outA, outB]).stdout.rstrip()

    def check_multi(self, Input: list[str], outA: list[str], outB: list[str]) -> list[str]: # returns result, failed testcase
        T = len(Input)
        if self.checker_code == None:
            return [default_checker.check_match(outA[i], outB[i]) for i in range(T)]
        else:
            outA_combined, outB_combined = f"{T}\n", f"{T}\n"
            Input_combined = f"{T}\n" + ''.join(Input)
            for i in range(T):
                outA_combined += normalize_lines(outA[i])
                outB_combined += normalize_lines(outB[i])
            return split_output(self.checker_code.execute(args=[Input_combined, outA_combined, outB_combined]).stdout)
    
    def customize_checker_if_needed(self, agent: Agent, statement: str) -> None:
        with open("instruction_texts/advanced_checker_requirement.txt", "r") as file:
            requirement_query = file.read()
        responce = agent.instruct(f"{statement}\n{requirement_query}")
        if "No" in responce[:10]:
            # Advanced checker is not needed
            return
        else:
            with open("instruction_texts/advanced_checker_gen.txt", "r") as file:
                prompt = file.read()
            self.checker_code = agent.instruct(prompt=prompt, code_only=True)
                
