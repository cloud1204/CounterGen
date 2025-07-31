class WorkFlow:
    def __init__(self, model_name, model_type, problem_statement, example_input = '', example_output = '', failed_code=''):
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output
        self.failed_code = failed_code

        self.generator = None
        self.validator = None
        self.checker = None
        self.AC_code = None
        from utils.agent import Agent
        self.agent = Agent(model_name, model_type)
    
    def validator_gen(self):
        prompt = f"Give me a python code that validates the testcase inputs for this problem:\n {self.problem_statement}\nIt should read input from stdin and print 'valid', or 'invalid' along with the violated constraint."
        self.validator = self.agent.instruct(prompt, code_only=True)

        while True:
            test_result = self.validator.execute(self.example_input)
            if test_result.stderr != '':
                prompt = (f"{test_result.stderr}\nPlease regenerate the validator code.")
            elif test_result.stdout.strip() != 'valid':
                prompt = (f"{self.example_input}\nThe validator say this testcase is invalid, but it should be valid.\nIt says {test_result.stdout}\nPlease regenerate the vaidator.") 
            else:
                # passed example test
                break
            self.validator = self.agent.instruct(prompt, code_only=True)
        print("Validator finished and tested.")
    
    def generator_gen(self):
        prompt = f"Give me a python code that generates valid random test inputs for this problem: {self.problem_statement}\nI need the input generator code only."
        self.generator = self.agent.instruct(prompt, code_only=True)

        GEN_TEST = 100
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
                    prompt = f"the validating result says the format is invalid. please give me the correct testcase generator code.\n{validator_result.stderr}"
                    succeed_flag = False
                    break
                elif validator_result.stdout.strip() != 'valid':
                    prompt = f"the validating result says the format is invalid. please give me the correct testcase generator code.\n{validator_result.stdout}"
                    succeed_flag = False
                    break
            if succeed_flag:
                # passed validator test
                break
            else:
                self.generator = self.agent.instruct(prompt, code_only=True)
        
        print("Generator finished and tested.")
                
    def work(self):
        self.validator_gen()
        self.generator_gen()

if __name__ == '__main__':
    with open("problem_info/statement.txt", "r") as file:
        problem_statement = file.read()
    with open("problem_info/example_input.txt", "r") as file:
        example_input = file.read()
    with open("problem_info/example_output.txt", "r") as file:
        example_output = file.read()
    tmp = WorkFlow('Gemini', 'default', problem_statement, example_input=example_input , example_output=example_output)
    tmp.work()