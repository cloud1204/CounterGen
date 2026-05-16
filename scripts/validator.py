from utils.agent import Agent
from utils.code import Code
import time

class Validator:
    def __init__(self, func_code: Code):
        self.namespace = {}
        try:
            exec(func_code.code, self.namespace)
        except Exception as e:
            raise ValueError(f"Validator code raised at load time: {e}") from e
        if 'validate' not in self.namespace or not callable(self.namespace['validate']):
            raise ValueError("Validator code did not define a callable 'validate' function.")
        self.validator_func = self.namespace['validate']
    def validate(self, testcase: str) -> str: # 'valid' or invalid reason
        return self.validator_func(testcase)
    def validate_multi(self, testcases: list[str]) -> list[str]:
        return [self.validate(tc) for tc in testcases]

class TC_Validator_Agent:
    def __init__(self, agent : Agent, problem_statement, example_input = '', example_output = ''):
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output
        self.validator_func = None
        self.args_limit = []
        self.agent = agent
    def _make_validator(self, prompt: str) -> Validator:
        last_err = None
        for _ in range(3):
            try:
                return Validator(self.agent.instruct(prompt, code_only=True))
            except (ValueError, AssertionError) as e:
                last_err = e
                print(f"Validator response could not be loaded ({e}). Asking again.")
                prompt = ("Your previous response could not be loaded. "
                          "Reply with a single ```python ...``` code block defining ONLY the "
                          "`validate(full_testcase: str) -> str` function. Do not include any "
                          "top-level statements, test calls, prints, or examples outside the function. "
                          + prompt)
        raise RuntimeError(f"Validator generation kept producing unloadable code: {last_err}")

    def work(self) -> Validator:
        start_time = time.time()
        prompt = f"Give me a python function named 'validate' that validates the testcase inputs for this problem:\n{self.problem_statement}\n \
            the format is: def validate(full_testcase: str)->str: It should return single 'valid', or 'invalid' + the violated constraint (combined as a single str).\
            Don't insert any comment in the code. Here is an example of valid input:\n{self.example_input}"

        validator = self._make_validator(prompt)

        succeed = False
        for _ in range(5):
            test_result = validator.validate(self.example_input)
            if test_result.strip() != 'valid':
                prompt = (f"{self.example_input}\nThe validator say this testcase is invalid, but it should be valid.\n\
                        It says {test_result}\nPlease regenerate the vaidator.")
                print(test_result)
                print('validator failed example testcases. Regenerating')
            else:
                succeed = True
                break
            validator = self._make_validator(prompt)
        if not succeed:
            raise RuntimeError("Failed to generate validator.")
        print(f"Validator finished and tested. Time spent: {time.time() - start_time} sec")
        return validator