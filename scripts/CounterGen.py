from utils.agent import Agent
from utils.common import Code
from scripts.tc_validator import TC_Validator_Agent
from scripts.tc_generator import TC_Generator_Agent
from scripts.stress_tester import Stress_Tester
from scripts.checker import Checker
from scripts.AC_generator import AC_Agent
def CounterGen(API_Option, API_Key, Statement, Input, Output, WA, AC) -> None:
    agent1 = None
    if API_Option == 'Gemini':
        # Use cheaper model for validator/generator (easier task)
        agent1 = Agent('Gemini', API_KEY=API_Key, model_type='2.5-flash')
    
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