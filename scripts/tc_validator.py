from utils.agent import Agent
from utils.common import Code
import time
class TC_Validator_Agent:
    def __init__(self, agent : Agent, problem_statement, example_input = '', example_output = ''):
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output

        self.validator = None

        self.args_limit = []
        self.agent = agent
    def work(self) -> Code:
        start_time = time.time()
        prompt = f"Give me a python code that validates the testcase inputs for this problem:\n{self.problem_statement}\n \
            It should read input from stdin and print 'valid', or 'invalid' along with the violated constraint.\
            Don't insert any comment in the code."
            
        self.validator = self.agent.instruct(prompt, code_only=True)

        while True:
            test_result = self.validator.execute(self.example_input)
            if test_result.stderr != '':
                prompt = (f"{test_result.stderr}\nPlease regenerate the validator code.")
            elif test_result.stdout.strip() != 'valid':
                prompt = (f"{self.example_input}\nThe validator say this testcase is invalid, but it should be valid.\n\
                        It says {test_result.stdout}\nPlease regenerate the vaidator.") 
            else:
                # passed example test
                break
            self.validator = self.agent.instruct(prompt, code_only=True)
        print(f"Validator finished and tested. Time spent: {time.time() - start_time} sec")
        return self.validator