from utils.code import Code, split_output
from scripts.checker import Checker
import math, random, time, os
import concurrent.futures as cf
class Stress_Tester:
    def __init__(self, generator: Code, args_limits: list[tuple[int, int]], AC_code: Code, failed_code: Code, checker: Checker) -> None:
        self.generator = generator
        self.args_limits = args_limits
        self.AC_code = AC_code
        self.failed_code = failed_code
        self.checker = checker
        self.current_best = ''
        self.fail_reason = ''
        pass
    def update_best_CE(self, test_input, fail_reason):
        if self.current_best == '' or len(test_input) < len(self.current_best):
            self.current_best = test_input
            self.fail_reason = fail_reason

    def stress_test(self, args):
        start_time = time.time()
        total_TL = 2
        cnt = 0
        T = 10
        succeed = False
        while True:
            cnt += T
            elapsed = time.time() - start_time
            if elapsed > total_TL:
                break
            test_inputs = split_output(self.generator.execute(args=args, input=f"{T}\n").stdout) 
            test_input_combined = f"{T}\n" + ''.join(test_inputs)
            # print("testcase\n" + test_input_combined)
            
            AC_output = self.AC_code.execute(input=test_input_combined, timeout=total_TL) ## might timeout as well
            if AC_output == 'timeout':
                print('AC Code TLEd')
                break
            else:
                AC_output = split_output(AC_output.stdout)

            client_output = self.failed_code.execute(input=test_input_combined, timeout=total_TL)
            if client_output == 'timeout':
                print('client code tled')
                break
            else:
                client_output = split_output(client_output.stdout)

            if len(client_output) < T:
                print(client_output)
                raise ValueError(f"client's program early exited during multi-test:\n{test_inputs[len(client_output)]}\n")
            test_result = self.checker.check_multi(test_inputs, client_output, AC_output)
            
            for i in range(T):
                if test_result[i] != 'AC':
                    #print(f"Counter Example found, size = {len(test_inputs[i])}, {test_result[i]}")
                    # if len(test_inputs[i]) < 50:
                    #     print(test_inputs[i])
                    self.update_best_CE(test_inputs[i], test_result[i])
                    succeed = True
            # if succeed:
            #     break
            T *= 2

        print(args)
        print(f"Tried {cnt} testcases")
        print("Successfully found counter example" if succeed else "Counter not found")
        return succeed
    def heatup(self):
        current_vector = [arg[0] for arg in self.args_limits]
        for t in range(15): #
            target = t % len(self.args_limits)
            new_value = current_vector[target] * 2 if current_vector[target] >= 5 else current_vector[target] + 1
            current_vector[target] = min(new_value, self.args_limits[target][1])

            if self.stress_test(current_vector):
                return current_vector


    def cooldown(self, current_vector):
        num_iterations = 10
        for t in range(num_iterations):
            new_vector = current_vector.copy()
            
            target = random.randint(0, len(new_vector) - 1)
            new_value = new_vector[target] // 2 if new_vector[target] >= 10 else new_vector[target] - 1
            new_vector[target] = max(new_value, self.args_limits[target][0])

            if self.stress_test(new_vector):
                current_vector = new_vector

        if self.current_best == '':
            print('Counter Example not found')

    def work(self):
        heated_up = self.heatup()
        self.cooldown(heated_up)