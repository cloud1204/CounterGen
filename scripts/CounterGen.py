from utils.agent import Agent
from utils.common import Code
from scripts.tc_validator import TC_Validator_Agent
from scripts.tc_generator import TC_Generator_Agent
from scripts.stress_tester import Stress_Tester
from scripts.checker import Checker
from scripts.AC_generator import AC_Agent
from utils.signal import Signal_Queue

class InvalidInputError(Exception):
    pass

def CounterGen(signal_queue: Signal_Queue, API_Option: str, API_Key: str, Statement: str, \
               Input: str, Output: str, WA: str, AC: str) -> None:

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
    
    validator = TC_Validator_Agent(agent1, Statement, Input, Output).work()
    generator, args_limit = TC_Generator_Agent(agent1, Statement, validator).work()
    
    failed_Code = Code(WA)
    checker = Checker()
    
    if AC == None or AC == '':
        if API_Option == 'Gemini':
            # Use stronger model for correct solution code
            agent2 = Agent('Gemini', API_KEY=API_Key, model_type='2.5-pro')
        AC_Code = AC_Agent(agent2, Statement, Input, Output, checker).work()
    else:
        AC_Code = Code(AC)

    tester = Stress_Tester(generator=generator, args_limits=args_limit, AC_code=AC_Code, failed_code=failed_Code) 
    tester.work()

    signal_queue.push(type='succ', msg=tester.current_best, field="ALL")