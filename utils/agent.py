class Agent:
    def __init__(self, model_name, model_type = 'default') -> None:
        if model_name == 'Gemini':
            from utils.gemini import Gemini_Agent
            self.Agent = Gemini_Agent(model_type)
        elif model_name == 'Chatgpt':
            pass
    def instruct(self, prompt, code_only = False):
        return self.Agent.instruct(prompt, code_only=code_only)
