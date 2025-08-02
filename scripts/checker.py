from scripts import default_checker
from utils.common import Code
class Checker:
    def __init__(self, checker_code : Code = None):
        self.checker_code = None
    def check(self, outA: str, outB: str) -> bool: # suppose outB is correct
        if self.checker_code == None:
            return default_checker.check_match(outputA=outA, outputB=outB)