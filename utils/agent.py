from utils.signal import Signal_Queue
class Agent:
    def __init__(self, signal_queue: Signal_Queue, model_name: str, 
                 API_KEY: str, model_type: str = 'default', description: str = '') -> None:
        if model_name == 'Gemini':
            from utils.gemini import Gemini_Agent
            self.Agent = Gemini_Agent(signal_queue=signal_queue, model_type=model_type, API_KEY=API_KEY)
        elif model_name == 'Chatgpt':
            raise ValueError(f'{model_name} is an unsupported model.')
        elif model_name == 'Claude':
            from utils.claude import Claude_Agent
            self.Agent = Claude_Agent(signal_queue=signal_queue, model_type=model_type, API_KEY=API_KEY)
        else:
            raise ValueError(f'{model_name} is an unsupported model.')
        
        print(f'{description} Successfully inited. {model_name} {model_type}')
    def instruct(self, prompt, code_only = False):
        return self.Agent.instruct(prompt, code_only=code_only)

