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

    def generator_gen(self):
        prompt = f"Give me a python code that generates valid random test inputs for this problem: {self.problem_statement}\nI need the input generator code only."
        self.generator = self.agent.instruct(prompt, code_only=True)
    
    def validator_gen(self):
        prompt = f"Give me a python code that validates the testcase inputs for this problem is valid. It should read input from stdin and print 'valid', or 'invalid' along with the invalid reason."
        self.validator = self.agent.instruct(prompt, code_only=True)

        while True:
            test_result = self.validator.execute(self.example_input)
            ## todo
            prompt = (f"Please read the problem again: {self.problem_statement}\nThe validator say this testcase is invalid, but it should be valid:\n{self.example_input}") 
            self.validator = self.agent.instruct(prompt, code_only=True)
        

