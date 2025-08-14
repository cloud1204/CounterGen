from utils.signal import Signal_Queue
class Agent:
    def __init__(self, signal_queue: Signal_Queue, model_name: str, API_KEY: str, model_type: str = 'default') -> None:
        if model_name == 'Gemini':
            from utils.gemini import Gemini_Agent
            self.Agent = Gemini_Agent(signal_queue=signal_queue, model_type=model_type, API_KEY=API_KEY)
        elif model_name == 'Chatgpt':
            # TODO
            pass
        elif model_name == 'Claude':
            # TODO
            pass
    def instruct(self, prompt, code_only = False):
        return self.Agent.instruct(prompt, code_only=code_only)

