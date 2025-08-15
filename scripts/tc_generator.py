from utils.agent import Agent
from utils.code import Code
import time
class TC_Generator_Agent:
    def __init__(self, agent: Agent, problem_statement: str, validator: Code):
        self.problem_statement = problem_statement
        self.validator = validator

        self.generator = None
        self.args_limit = []
        self.agent = agent
    
    def work(self) -> tuple[Code, list[tuple[int, int]]]:
        start_time = time.time()

        prompt = f"Give me a python code that generates (via print) valid random test inputs for this problem: {self.problem_statement}\n\
            I need the input generator code only, and don't insert any comment in the code."
        self.generator = self.agent.instruct(prompt, code_only=True)

        GEN_TEST = 5
        while True:
            succeed_flag = True
            for t in range(GEN_TEST):
                generated_tc = self.generator.execute()
                if generated_tc.stderr:
                    prompt = f"something went wrong when generating\n:{generated_tc.stderr}. Please give me the correct generator code."
                    succeed_flag = False
                    break
                validator_result = self.validator.execute(generated_tc.stdout)
                if validator_result.stderr:
                    prompt = f"the validating result says the format is invalid. please give me the correct testcase generator code.\n\
                        {validator_result.stderr}"
                    succeed_flag = False
                    break
                elif validator_result.stdout.strip() != 'valid':
                    prompt = f"the validating result says the format is invalid. please give me the correct testcase generator code.\
                        \n{validator_result.stdout}"
                    succeed_flag = False
                    break
            if succeed_flag:
                # passed validator test
                break
            else:
                print("Generator failed validating. Try again.")
                self.generator = self.agent.instruct(prompt, code_only=True)
        
        print(f"Baseline Generator finished. Time spent: {time.time() - start_time} sec")
        start_time = time.time()

        with open("instruction_texts/advanced_tc_gen.txt", "r") as file:
            prompt = file.read()
        self.generator = self.agent.instruct(prompt, code_only=True)
        prompt = "Now, give me a list of the args limits (tuples of ranges) that satisfy this problem's input constraints, \
            like [(1, 100), (1, 10000), (1, 1000000000)] for my example above. Give me the python list only, \
                do not include any explanation or extra text. Please ensure that the args would satisfy the problem constraint"
        self.args_limit = eval(self.agent.instruct(prompt, code_only=True).code)

        while True:
            succeed_flag = True
            for t in range(GEN_TEST):
                import random
                test_args = [random.randint(self.args_limit[i][0], self.args_limit[i][1]) \
                             for i in range(len(self.args_limit))]
                print('testing', test_args)
                generated_tc = self.generator.execute(args=test_args, timeout=5)
                if generated_tc == 'timeout':
                    prompt = f"The generator timeouted with this args: {test_args}\nGive me the generator code that generate valid testcases for any args satisfying the ranges."
                    succeed_flag = False
                    break
                if generated_tc.stderr:
                    prompt = f"something went wrong when generating with this args: {str(test_args)}\n:{generated_tc.stderr}. Please give me the correct generator code."
                    succeed_flag = False
                    break
                validator_result = self.validator.execute(generated_tc.stdout)
                if validator_result.stderr:
                    prompt = f"with this args: {str(test_args)}, the validating result says the testcase format is invalid.\
                        Give me the generator code that generate valid testcases for any args satisfying the ranges.\n{validator_result.stderr}"
                    succeed_flag = False
                    break
                elif validator_result.stdout.strip() != 'valid':
                    prompt = f"with this args: {str(test_args)}, the validating result says the testcase format is invalid.\
                        Give me the generator code that generate valid testcases for any args satisfying the ranges.\n{validator_result.stdout}"
                    succeed_flag = False
                    break
            if succeed_flag:
                # passed validator test
                break
            else:
                print("Generator failed validating. Try again.")
                self.generator = self.agent.instruct(prompt, code_only=True)
        print(f"Advanced Generator finished and tested. args: {str(self.args_limit)}\n Time spent: {time.time() - start_time} sec")
        return self.generator, self.args_limit