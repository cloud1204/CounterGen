class Agent:
    def __init__(self, model_name, API_KEY, model_type = 'default') -> None:
        if model_name == 'Gemini':
            from utils.gemini import Gemini_Agent
            self.Agent = Gemini_Agent(model_type=model_type, API_KEY=API_KEY)
        elif model_name == 'Chatgpt':
            # TODO
            pass
        elif model_name == 'Claude':
            # TODO
            pass
    def instruct(self, prompt, code_only = False):
        return self.Agent.instruct(prompt, code_only=code_only)

