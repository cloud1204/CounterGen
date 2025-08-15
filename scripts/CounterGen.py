from utils.agent import Agent
from utils.code import Code
from scripts.tc_validator import TC_Validator_Agent
from scripts.tc_generator import TC_Generator_Agent
from scripts.stress_tester import Stress_Tester
from scripts.checker import Checker
from scripts.AC_generator import AC_Agent
from utils.signal import Signal_Queue
import os, time
from concurrent.futures import ThreadPoolExecutor

class InvalidInputError(Exception):
    pass

def checker_gen(signal_queue: Signal_Queue, agent, Statement) -> Checker:
    signal_queue.push(type='start', msg="Start Generating Checker", field="Checker")
    checker = Checker()
    checker.customize_checker_if_needed(agent=agent, statement=Statement)
    print('Checker finished')
    signal_queue.push(type='succ', msg="Successfully Generated Checker", field="Checker")
    return checker

def validator_gen(signal_queue: Signal_Queue, agent, Statement, Input, Output):
    signal_queue.push(type='start', msg="Start generating validator", field="Validator")
    validator = TC_Validator_Agent(agent, Statement, Input, Output).work()
    signal_queue.push(type='succ', msg="Successfully generated and tested validator", field="Validator")
    return validator
def generator_gen(signal_queue: Signal_Queue, agent, Statement, validator):
    signal_queue.push(type='start', msg="Start generating generator", field="Generator")
    generator, args_limit = TC_Generator_Agent(agent, Statement, validator).work()
    signal_queue.push(type='succ', msg="Successfully generated and tested generator", field="Generator")
    return generator, args_limit
def AC_Code_gen(signal_queue: Signal_Queue, AC_agent: AC_Agent):
    signal_queue.push(type='start', msg="Start generating AC Code", field="AC Code")
    return AC_agent.generate_first_edition()
def AC_Code_test(signal_queue: Signal_Queue, AC_agent: AC_Agent):
    result = AC_agent.test()
    signal_queue.push(type='succ', msg="Successfully Generated and tested AC Code", field="AC Code")
    return result

def CounterGen(signal_queue: Signal_Queue, settings: dict, Statement: str, \
               Input: str, Output: str, WA: str, AC: str) -> None:
    if not os.path.exists("./tmp_storage"):
        os.makedirs("./tmp_storage")
    for filename in os.listdir("./tmp_storage"):
        file_path = os.path.join("./tmp_storage", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    start_time = time.time()

    try:
        failed_Code = Code(WA)
        failed_Code.wrap()
        print("User's code successfully compiled.")
    except Exception as e:
        print(e)
        print("User's code compilation failed. Please make sure it is valid c++/python code.")
        return

    model_name = settings['Last_Use']
    API_Key = settings[model_name]['API_KEY']
    
    if AC != None and AC != '':
        try:
            AC_Code = Code(AC)
            signal_queue.push(type='succ', msg="Successfully Compiled AC Code", field="AC Code")
        except Exception as e:
            signal_queue.push(type='fail', msg=f"{e}\nTry again.", field="AC Code")
            return
    try:
        model_type = settings[model_name]['val/gen']
        agent1 = Agent(signal_queue=signal_queue, model_name=model_name, 
                       API_KEY=API_Key, model_type=model_type, desctiption="Validator/Generator Agent")
    except Exception as e:
        signal_queue.push(type='fail', msg=f"{e}\nTry again.", field="API")
        return
    
    try:
        model_type = settings[model_name]['checker']
        agent2 = Agent(signal_queue=signal_queue, model_name=model_name, 
                       API_KEY=API_Key, model_type=model_type, desctiption="Checker Agent")
    except Exception as e:
        signal_queue.push(type='fail', msg=f"{e}\nTry again.", field="API")
        return
    
    if AC != None and AC != '':
        signal_queue.push(type='succ', msg="successfully initalized chat", field="API")

    with ThreadPoolExecutor() as executor:
        fVAL = executor.submit(validator_gen, signal_queue, agent1, Statement, Input, Output)
        fCHE = executor.submit(checker_gen, signal_queue, agent2, Statement)
        if AC == None or AC == '':
            model_type = settings[model_name]['AC']
            try:
                agent3 = Agent(signal_queue=signal_queue, model_name=model_name, 
                               API_KEY=API_Key, model_type=model_type, desctiption="AC Agent")
            except Exception as e:
                signal_queue.push(type='fail', msg=f"{e}\nTry again.", field="API")
                return
            
            signal_queue.push(type='succ', msg="successfully initalized chat", field="API")
            
            AC_agent = AC_Agent(agent3, Statement, Input, Output)
            fAC = executor.submit(AC_Code_gen, signal_queue, AC_agent)

        validator = fVAL.result()

        fGEN = executor.submit(generator_gen, signal_queue, agent1, Statement, validator)

        checker = fCHE.result()
        if (AC == None or AC == '') and fAC.result():
            AC_agent.set_checker(checker=checker)
            fAC = executor.submit(AC_Code_test, signal_queue, AC_agent)

        generator, args_limit = fGEN.result()

        if AC == None or AC == '':
            AC_Code = fAC.result()
        
    generator.wrap()
    AC_Code.wrap()
    
    signal_queue.push(type='start', msg='Start Stress Testing', field="Stress Test")

    tester = Stress_Tester(generator=generator, args_limits=args_limit, AC_code=AC_Code, failed_code=failed_Code,
                            checker=checker, signal_queue=signal_queue, TL_batch=settings['Time_Limit_Per_Batch']) 
    tester.work()

    print(f"Successfully found counter example. Total time spent: {time.time() - start_time} sec")
    signal_queue.push(type='succ', msg=(tester.current_best, tester.fail_reason), field="Stress Test")
    for filename in os.listdir("./tmp_storage"):
        file_path = os.path.join("./tmp_storage", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)