from utils.agent import Agent
from utils.code import Code
from scripts.checker import Checker
from scripts.metamorphic import Metamorphic
import time
class AC_Agent:
    def __init__(self, agent : Agent, problem_statement : str, example_input : str, example_output : str):
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output
        self.checker = None
        self.metamorphic: Metamorphic = None

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

    def set_metamorphic(self, metamorphic):
        self.metamorphic = metamorphic

    def _metamorphic_check(self, original_stdout: str):
        if self.metamorphic is None:
            return None
        try:
            transformed = self.metamorphic.transform(self.example_input)
        except Exception as e:
            print(f"Metamorphic check: transform raised {e}. Skipping this round.")
            return None
        new_run = self.AC_code.execute(transformed)
        if new_run == 'timeout':
            return f"AC code timed out on transformed input:\n{transformed}"
        if new_run.stderr or new_run.returncode != 0:
            return f"AC code crashed on transformed input:\n{transformed}\nstderr: {new_run.stderr}"
        try:
            verdict = self.metamorphic.relate(self.example_input, original_stdout, transformed, new_run.stdout)
        except Exception as e:
            print(f"Metamorphic check: relate raised {e}. Skipping this round.")
            return None
        if isinstance(verdict, str) and verdict.strip() == 'OK':
            return None
        return (f"On transformed input:\n{transformed}\n"
                f"the AC output was:\n{new_run.stdout}\n"
                f"and the metamorphic check failed with reason: {verdict}\n"
                f"(reference input was:\n{self.example_input}\nwith reference output:\n{original_stdout})")

    def test(self) -> Code:
        assert self.AC_code != None and self.checker != None
        start_time = time.time()
        succeed = False
        MAX_TRY = 3
        for _ in range(MAX_TRY):
            test_output = self.AC_code.execute(self.example_input)
            if test_output.stderr != '':
                print("AC Code went wrong. Try again.")
                prompt = f"{test_output.stderr}\n give me the correct whole python code"
                self.AC_code = self.agent.instruct(prompt, code_only=True)
                continue
            test_result = self.checker.check(self.example_input, test_output.stdout, self.example_output)
            if test_result != 'AC':
                print(f"AC Code failed example input. Try again. {test_result}")
                prompt = f"The code isnt correct. On this testcase:\n{self.example_input}\n{test_result}\nYou can assume there is only very small inputs, so you can use a super naive method (prioritize the correctness) to solve it. \
                    give me the correct whole python code. Dont insert any comment in the code"
                self.AC_code = self.agent.instruct(prompt, code_only=True)
                continue

            meta_reason = self._metamorphic_check(test_output.stdout)
            if meta_reason is not None:
                print(f"AC Code passed example IO but failed metamorphic test.\n{meta_reason}")
                prompt = (f"The code is incorrect. {meta_reason}\n"
                          f"Give me the corrected whole python code. Prioritize correctness; a brute-force "
                          f"method is fine. Don't insert any comment in the code.")
                self.AC_code = self.agent.instruct(prompt, code_only=True)
                continue

            succeed = True
            break
        if not succeed:
            raise RuntimeError(f"Failed to generate AC Code in {MAX_TRY} tries. You should try a stronger model.")
        print(f"AC code finished and tested. Time spent: {time.time() - start_time} sec")
        return self.AC_code
