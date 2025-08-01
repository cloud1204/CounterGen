from default_checker import check_match
import time
class WorkFlow:
    def __init__(self, model_name, model_type, problem_statement, example_input = '', example_output = '', failed_code='', AC_code = ''):
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output
        self.failed_code = failed_code

        self.generator = None
        self.validator = None
        self.checker = None
        self.AC_code = AC_code

        self.args_limit = []
        from utils.agent import Agent
        self.agent = Agent(model_name, model_type)

        self.agent_AC = Agent(model_name, '2.5-pro')


    
    def validator_gen(self):
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
    
    def generator_gen(self):
        start_time = time.time()

        prompt = f"Give me a python code that generates valid random test inputs for this problem: {self.problem_statement}\n\
            I need the input generator code only, and don't insert any comment in the code."
        self.generator = self.agent.instruct(prompt, code_only=True)

        GEN_TEST = 10
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
        
        print(f"Baseline Generator finished and tested. Time spent: {time.time() - start_time} sec")
        start_time = time.time()

        with open("instruction_texts/advanced_tc_gen.txt", "r") as file:
            prompt = file.read()
        self.generator = self.agent.instruct(prompt, code_only=True)
        prompt = "Now, give me a list of the args limits (tuples of ranges) that satisfy this problem's input constraints, \
            like [(1, 100), (1, 10000), (1, 1000000000)] for my example above. Give me the python list only, \
                do not include any explanation or extra text."
        self.args_limit = eval(self.agent.instruct(prompt, code_only=True).code)

        GEN_TEST = 10
        while True:
            succeed_flag = True
            for t in range(GEN_TEST):
                import random
                test_args = [random.randint(self.args_limit[i][0], self.args_limit[i][1]) for i in range(len(self.args_limit))]
                generated_tc = self.generator.execute(args=test_args)
                if generated_tc.stderr:
                    prompt = f"something went wrong when generating with this args: {str(test_args)}\n:{generated_tc.stderr}. Please give me the correct generator code."
                    succeed_flag = False
                    break
                validator_result = self.validator.execute(generated_tc.stdout)
                if validator_result.stderr:
                    prompt = f"with this args: {str(test_args)}, the validating result says the testcase format is invalid. please give me the correct testcase generator code.\n\
                        {validator_result.stderr}"
                    succeed_flag = False
                    break
                elif validator_result.stdout.strip() != 'valid':
                    prompt = f"with this args: {str(test_args)}, the validating result says the testcase format is invalid. please give me the correct testcase generator code.\
                        \n{validator_result.stdout}"
                    succeed_flag = False
                    break
            if succeed_flag:
                # passed validator test
                break
            else:
                print("Generator failed validating. Try again.")
                self.generator = self.agent.instruct(prompt, code_only=True)
        print(f"Advanced Generator finished and tested. args: {str(self.args_limit)}\n Time spent: {time.time() - start_time} sec")




    def AC_gen(self):
        start_time = time.time()
        if self.AC_code != '':
            return
        print('AC Code not found, generating AC Code')
        prompt = f"Now, please give me a correct python code to solve this problem:\n{self.problem_statement}\n\
            you can suppose the constraint is much smaller than it said and use a super naive method (prioritize the correctness) to solve it. \
                don't insert any comment in the code."
        self.AC_code = self.agent_AC.instruct(prompt, code_only=True)
        while True:
            test_output = self.AC_code.execute(self.example_input)
            if test_output.stderr != '':
                print("AC Code went wrong. Try again.")
                prompt = f"{test_output.stderr}\n give me the correct whole python code"
                self.AC_code = self.agent_AC.instruct(prompt, code_only=True)
            elif not check_match(test_output.stdout, self.example_output):
                print("AC Code failed example input. Try again.")
                prompt = f"The code isnt correct. you can use a more naive method (prioritize the correctness) to solve it. \
                    give me the correct whole python code."
                self.AC_code = self.agent_AC.instruct(prompt, code_only=True)
            else:
                # passed example input
                break
        print(f"AC code finished and tested. Time spent: {time.time() - start_time} sec")

        
                
    def work(self):
        self.validator_gen()
        self.generator_gen()
        self.AC_gen()
from utils.common import Code
from tc_optimizer import optimizer
if __name__ == '__main__':
    with open("problem_info/statement.txt", "r") as file:
        problem_statement = file.read()
    with open("problem_info/example_input.txt", "r") as file:
        example_input = file.read()
    with open("problem_info/example_output.txt", "r") as file:
        example_output = file.read()
    # with open("problem_info/AC.py", "r") as file:
    #     AC_Code = Code(file.read())
    with open("problem_info/WA.py", "r") as file:
        WA_Code = Code(file.read())


    tmp = WorkFlow('Gemini', 'default', problem_statement, example_input=example_input, example_output=example_output)
    tmp.work()
        
    # with open("test_gen.py", "r") as file:
    #     generator = Code(file.read())
    # with open("test_valid.py", "r") as file:
    #     validator = Code(file.read())
    # args_limit = [(1, 10000), (1, 300000), (1, 300000)]

    opt = optimizer(tmp.generator, tmp.args_limit, tmp.AC_code, WA_Code)
    opt.optimize()