from utils.code import Code, split_output
from utils.signal import Signal_Queue
from scripts.checker import Checker
import math, random, time, os
import concurrent.futures as cf
class Stress_Tester:
    def __init__(self, generator: Code, args_limits: list[tuple[int, int]], AC_code: Code,
                 failed_code: Code, checker: Checker, signal_queue: Signal_Queue, TL_batch = 2) -> None:
        self.generator = generator
        self.args_limits = args_limits
        self.AC_code = AC_code
        self.failed_code = failed_code
        self.checker = checker
        self.signal_queue = signal_queue
        self.TL_batch = TL_batch
        self.current_best = ''
        self.fail_reason = ''
        pass
    def update_best_CE(self, test_input, fail_reason) -> bool:
        if self.current_best == '' or len(test_input) < len(self.current_best):
            self.current_best = test_input
            self.fail_reason = fail_reason
            return True
        else:
            return False


    def stress_test(self, args):
        start_time = time.time()
        total_TL = self.TL_batch
        cnt = 0
        T = 10
        succeed = False
        print(args)
        while True:
            if self.signal_queue.shutdown_is_set():
                raise TimeoutError("Stress Tester shutting down")
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
            if len(test_inputs) != T:
                print(test_inputs)
                raise ValueError(f"Something went wrong. The testcase number did not match.")
            if len(AC_output) != T:
                print(client_output)
                if len(AC_output) < T:
                    raise ValueError(f"Judge's program early exited during multi-test:\n{test_inputs[len(client_output)]}\n")
                else:
                    raise ValueError(f"Judge's program outputted more than T testcases:\n{test_inputs}\n")
            if len(client_output) != T:
                if T < 200:
                    print(test_inputs)

                print(client_output)
                print(len(client_output))
                if len(client_output) < T:
                    raise ValueError(f"Client's program early exited during multi-test:\n{test_inputs[len(client_output)]}\n")
                else:
                    raise ValueError(f"Client's program outputted more than T testcases:\n{test_inputs}\n")
            test_result = self.checker.check_multi(test_inputs, client_output, AC_output)
            
            for i in range(T):
                if test_result[i] != 'AC':
                    is_best = self.update_best_CE(test_inputs[i], test_result[i])
                    succeed |= is_best
                    if is_best:
                        print('Current Best CE:\n' + test_inputs[i] + '\n' + test_result[i])
            T *= 2

        print(f"Tried {cnt} testcases")
        if succeed:
            print("Successfully updated counter example")
        else:
            print("Counter example not updated" if self.current_best != '' else "Counter example not found")
        return succeed
    def heatup(self):
        current_vector = [arg[0] for arg in self.args_limits]
        for t in range(50): #
            target = t % len(self.args_limits)
            new_value = current_vector[target] * 3 if current_vector[target] >= 5 else current_vector[target] + 1
            current_vector[target] = min(new_value, self.args_limits[target][1])

            if self.stress_test(current_vector):
                return current_vector


    def cooldown(self, current_vector):
        num_iterations = 15
        chances = 5
        for t in range(num_iterations):
            new_vector = current_vector.copy()
            
            target = random.randint(0, len(new_vector) - 1)
            new_value = new_vector[target] // 2 if new_vector[target] >= 10 else new_vector[target] - 1
            new_vector[target] = max(new_value, self.args_limits[target][0])

            if self.stress_test(new_vector):
                current_vector = new_vector
                chances = 5
            else:
                chances -= 1
            if chances == 0: # Early stop
                break

    def work(self):
        heated_up = self.heatup()
        if self.current_best == '':
            print('Counter Example not found')
            return
        self.cooldown(heated_up)