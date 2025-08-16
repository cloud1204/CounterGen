from utils.agent import Agent
from utils.code import Code
from scripts.checker import Checker
import time
class AC_Agent:
    def __init__(self, agent : Agent, problem_statement : str, example_input : str, example_output : str):
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output
        self.checker = None

        self.agent = agent
        self.AC_code = ''
    def generate_first_edition(self):
        start_time = time.time()
        print('AC Code not found, generating AC Code')
        prompt = f"Please give me a correct python code to solve this problem:\n{self.problem_statement}\n\
            you can use a brute-force method (prioritize the correctness) to solve it. Don't insert any comment in the code.\n"
        self.AC_code = self.agent.instruct(prompt, code_only=True)
        print(f"AC code first edition generated. Time spent: {time.time() - start_time} sec")
        return True
    def set_checker(self, checker: Checker):
        self.checker = checker

    def test(self) -> Code:
        assert self.AC_code != None and self.checker != None
        start_time = time.time()
        succeed = False
        for _ in range(5):
            test_output = self.AC_code.execute(self.example_input)
            if test_output.stderr != '':
                print("AC Code went wrong. Try again.")
                prompt = f"{test_output.stderr}\n give me the correct whole python code"
                self.AC_code = self.agent.instruct(prompt, code_only=True)
                continue
            test_result = self.checker.check(self.example_input, test_output.stdout, self.example_output)
            if test_result != 'AC':
                print(f"AC Code failed example input. Try again. {test_result}")
                prompt = f"The code isnt correct. for this testcase:\
                    {self.example_input}\n{test_result}\nYou can use a more naive method (prioritize the correctness) to solve it. \
                    give me the correct whole python code. Dont insert any comment in the code"
                self.AC_code = self.agent.instruct(prompt, code_only=True)
            else:
                succeed = True
                break
        if not succeed:
            raise RuntimeError("Failed to generate AC Code in 6 tries.")
        print(f"AC code finished and tested. Time spent: {time.time() - start_time} sec")
        return self.AC_code
