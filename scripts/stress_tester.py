from utils.common import Code
from scripts.default_checker import check_match
import math, random
class Stress_Tester:
    def __init__(self, generator: Code, args_limits: list[tuple[int, int]], AC_code: Code, failed_code: Code) -> None:
        self.generator = generator
        self.args_limits = args_limits
        self.AC_code = AC_code
        self.failed_code = failed_code
        self.current_best = ''
        pass
    def update_best_CE(self, test_input):
        if self.current_best == '' or len(test_input) < len(self.current_best):
            self.current_best = test_input
    def stress_test(self, args):
        import time
        start_time = time.time()
        total_TL = 3
        single_TL = 1
        cnt = 0
        succeed = False
        while True:
            cnt += 1
            elapsed = time.time() - start_time
            if elapsed > total_TL:
                break
            time_left = max(total_TL - elapsed, single_TL)
            test_input = self.generator.execute(args=args).stdout 
            AC_output = self.AC_code.execute(input=test_input, timeout=time_left).stdout ## might timeout as well
            if AC_output == 'timeout':
                print('AC Code TLEd')
                break
            client_output = self.failed_code.execute(input=test_input, timeout=time_left).stdout
            if client_output == 'timeout':
                print('AC Code TLEd')
                self.update_best_CE(test_input)
                succeed = True
                break
            if not check_match(client_output, AC_output):
                print(f"Counter Example found, size = {len(test_input)}")
                if len(test_input) < 50:
                    print(test_input)
                self.update_best_CE(test_input)
                succeed = True
                break
        print(args)
        print(f"Tried {cnt} testcases")
        return succeed
    def heatup(self):
        current_vector = [arg[0] for arg in self.args_limits]
        for t in range(1000):
            target = t % len(self.args_limits)
            new_value = current_vector[target] * 2 if current_vector[target] >= 5 else current_vector[target] + 1
            current_vector[target] = min(new_value, self.args_limits[target][1])

            if self.stress_test(current_vector):
                return current_vector


    def cooldown(self, current_vector):
        num_iterations = 15
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