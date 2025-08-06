from utils.agent import Agent
from utils.common import Code
from scripts.tc_validator import TC_Validator_Agent
from scripts.tc_generator import TC_Generator_Agent
from scripts.stress_tester import Stress_Tester
from scripts.checker import Checker
from scripts.AC_generator import AC_Agent
from utils.signal import Signal_Queue
import os
from concurrent.futures import ThreadPoolExecutor

class InvalidInputError(Exception):
    pass
def validator_gen(agent, Statement, Input, Output):
    validator = TC_Validator_Agent(agent, Statement, Input, Output).work()
    return validator
def generator_gen(agent, Statement, validator):
    generator, args_limit = TC_Generator_Agent(agent, Statement, validator).work()
    return generator, args_limit
def AC_Code_gen(agent: Agent, Statement: str, Input: str, Output: str, checker: Checker):
    return AC_Agent(agent, Statement, Input, Output, checker).work()

def CounterGen(signal_queue: Signal_Queue, API_Option: str, API_Key: str, Statement: str, \
               Input: str, Output: str, WA: str, AC: str) -> None:
    

    failed_Code = Code(WA)
    checker = Checker()
    
    if AC != None and AC != '':
        try:
            AC_Code = Code(AC)
            signal_queue.push(type='succ', msg="Successfully Compiled AC Code", field="AC Code")
        except Exception as e:
            signal_queue.push(type='fail', msg=f"{e}\nTry again.", field="AC Code")
            return
    try:
        if API_Option == 'Gemini':
            # Use cheaper model for validator/generator (easier task)
            agent1 = Agent('Gemini', API_KEY=API_Key, model_type='2.5-flash')
        else:
            raise InvalidInputError('Unsupported API Type.')
    except Exception as e:
        signal_queue.push(type='fail', msg=f"{e}\nTry again.", field="API")
        return

    signal_queue.push(type='succ', msg="successfully initalized chat", field="API")

    with ThreadPoolExecutor() as executor:
        fVAL = executor.submit(validator_gen, agent1, Statement, Input, Output)
        if AC == None or AC == '':
            if API_Option == 'Gemini':
                # Use stronger model for correct solution code
                agent2 = Agent('Gemini', API_KEY=API_Key, model_type='2.5-pro')
            else:
                raise InvalidInputError('Unsupported API Type.')
            fb = executor.submit(AC_Code_gen, agent2, Statement, Input, Output, checker)

        validator = fVAL.result()
        signal_queue.push(type='succ', msg="Successfully generated and tested validator", field="Validator")

        fGEN = executor.submit(generator_gen, agent1, Statement, validator)

        generator, args_limit = fGEN.result()
        signal_queue.push(type='succ', msg="Successfully generated and tested generator", field="Generator")

        if AC == None or AC == '':
            AC_Code = fb.result()
            signal_queue.push(type='succ', msg="Successfully Generated and tested AC Code", field="AC Code")
        

    tester = Stress_Tester(generator=generator, args_limits=args_limit, AC_code=AC_Code, failed_code=failed_Code) 
    tester.work()

    signal_queue.push(type='succ', msg=tester.current_best, field="Stress Test")
    for filename in os.listdir("./tmp_storage"):
        file_path = os.path.join("./tmp_storage", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)