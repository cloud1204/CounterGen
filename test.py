# from utils.agent import Agent

# gemini_agent = Agent('Gemini')

# with open("statement.txt", "r") as file:
#     problem_statement = file.read()
#     prompt = f"Give me a python code that generates valid random test inputs for this problem: {problem_statement}\nI need the input generator code only."

# print(gemini_agent.instruct(prompt))

# print(gemini_agent.instruct("now, give me a correct AC solution code for it."))

from utils.common import Code
print(len(Code('t```print(1```').execute().stderr))