from utils.agent import Agent
from utils.common import Code
from scripts.checker import Checker
import time
class AC_Agent:
    def __init__(self, agent : Agent, problem_statement : str, example_input : str, example_output : str, checker: Checker):
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output
        self.checker = checker

        self.agent = agent
        self.AC_code = ''

    def work(self) -> Code:
        start_time = time.time()
        print('AC Code not found, generating AC Code')
        prompt = f"Please give me a correct python code to solve this problem:\n{self.problem_statement}\n\
            you can suppose the constraint is much smaller than it said and use a super naive method (prioritize the correctness) to solve it. \
                don't insert any comment in the code."
        self.AC_code = self.agent.instruct(prompt, code_only=True)
        while True:
            test_output = self.AC_code.execute(self.example_input)
            if test_output.stderr != '':
                print("AC Code went wrong. Try again.")
                prompt = f"{test_output.stderr}\n give me the correct whole python code"
                self.AC_code = self.agent.instruct(prompt, code_only=True)
            elif not self.checker.check(test_output.stdout, self.example_output):
                print("AC Code failed example input. Try again.")
                prompt = f"The code isnt correct. the correct output for this testcase:\
                    {self.example_input}\n should be\n{self.example_output}\nYou can use a more naive method (prioritize the correctness) to solve it. \
                    give me the correct whole python code."
                self.AC_code = self.agent.instruct(prompt, code_only=True)
            else:
                break
        print(f"AC code finished and tested. Time spent: {time.time() - start_time} sec")
        return self.AC_code
