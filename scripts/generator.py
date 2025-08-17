from utils.agent import Agent
from utils.code import Code, split_output
from scripts.validator import Validator
import time, math, random
def small_args_limits(args_limit):
    result = []
    for l, r in args_limit:
        result.append((l, max(l, min(math.floor(math.sqrt(r)), r))))
    return result
class Generator_Agent:
    def __init__(self, agent: Agent, problem_statement: str, example_input : str):
        self.problem_statement = problem_statement
        self.generator = None
        self.args_limit = []
        self.agent = agent
        self.example_input = example_input

    def generate_first_edition(self):
        prompt = f"Give me a python code that generates (via print) valid random test inputs for this problem: {self.problem_statement}\n\
            I need the input generator code only, and don't insert any comment in the code. Example input: {self.example_input}\n"
        self.generator = self.agent.instruct(prompt, code_only=True)
        self.generator.wrap()
        return True
    
    def finalize(self, validator: Validator) -> tuple[Code, list[tuple[int, int]]]:
        start_time = time.time()

        GEN_TEST = 5
        while True:
            succeed_flag = True
            T = 10
            generated_tc = self.generator.execute(input=f"{T}\n")
            if generated_tc.stderr:
                prompt = f"something went wrong when generating\n:{generated_tc.stderr}. Please give me the correct generator code."
                succeed_flag = False
                break
            validator_result = validator.validate_multi(split_output(generated_tc.stdout))
            for i in range(T):
                if validator_result[i].strip() != 'valid':
                    print(split_output(generated_tc.stdout)[i])
                    print(validator_result[i])
                    prompt = f"the validating result says the format is invalid. please give me the correct testcase generator code.\
                        \n{validator_result[i]}"
                    succeed_flag = False
                    break
            if succeed_flag:
                # passed validator test
                break
            else:
                print("Baseline Generator failed validating. Try again.")
                self.generator = self.agent.instruct(prompt, code_only=True)
                self.generator.wrap()
        
        print(f"Baseline Generator finished. Time spent: {time.time() - start_time} sec")
        start_time = time.time()

        with open("instruction_texts/advanced_tc_gen.txt", "r") as file:
            prompt = file.read()
        self.generator = self.agent.instruct(prompt, code_only=True)
        self.generator.wrap()
        prompt = "Now, give me a list of the args limits (tuples of ranges) so that we can control the testcase size while \
            satisfying this problem's input constraints, like [(1, 100), (1, 10000), (1, 1000000000)] for my example above. \
                Give me the python list only, do not include any explanation or extra text."
        self.args_limit = eval(self.agent.instruct(prompt, code_only=True).code)

        while True:
            succeed_flag = True
            for _ in range(GEN_TEST):
                if _ == 0:
                    args_limits = [(args[0], args[0]) for args in self.args_limit]
                    T = 10
                elif _ <= GEN_TEST // 2:
                    args_limits = small_args_limits(self.args_limit)
                    T = 100
                else:
                    args_limits = self.args_limit
                    T = 5
                test_args = [random.randint(l, r) for l, r in args_limits]
                print('testing', test_args)

                generated_tc = self.generator.execute(input = f"{T}\n", args=test_args, timeout=5)
                if generated_tc == 'timeout':
                    prompt = f"The generator timeouted with this args: {test_args}\nGive me the generator code that generate valid testcases for any args satisfying the ranges."
                    succeed_flag = False
                    break
                if generated_tc.stderr:
                    prompt = f"something went wrong when generating with this args: {str(test_args)}\n:{generated_tc.stderr}. Please give me the correct generator code."
                    succeed_flag = False
                    break
                generated_tc = split_output(generated_tc.stdout)
                validator_result = validator.validate_multi(generated_tc)
                for i in range(T):
                    if validator_result[i].strip() != 'valid':
                        prompt = f"with this args: {str(test_args)}, the validating result says the testcase format is invalid.\
                            Give me the generator code that generate valid testcases for any args satisfying the ranges.\n{validator_result[i]}"
                        succeed_flag = False
                        break
                if not succeed_flag:
                    break
            if succeed_flag:
                # passed validator test
                break
            else:
                print("Generator failed validating. Try again.")
                self.generator = self.agent.instruct(prompt, code_only=True)
                self.generator.wrap()
        print(f"Advanced Generator finished and tested. args: {str(self.args_limit)}\n Time spent: {time.time() - start_time} sec")
        return self.generator, self.args_limit