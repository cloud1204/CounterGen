from scripts import default_checker
from utils.code import Code
from utils.agent import Agent
import re
def has_invalid_control_chars(s):
    # Control characters: ASCII 0–31, exclude \n (10) and optionally \t (9)
    return bool(re.search(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', s))
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
                
