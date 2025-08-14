import utils.code as code
from utils.signal import Signal_Queue
import threading
from utils.signal import Signal_Queue
class Gemini_Agent:
    def __init__(self, signal_queue: Signal_Queue,API_KEY: str, model_type : str ='default'):
        self.signal_queue = signal_queue
        import google.generativeai as genai
        import yaml
        genai.configure(api_key=API_KEY)
        if model_type == '2.5-pro':
            self.model = genai.GenerativeModel("gemini-2.5-pro")
        elif model_type == 'default' or model_type == '2.5-flash':
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.chat = self.model.start_chat()
    def instruct(self, prompt, code_only = False):
        response_holder = {}
        def target():
            response_holder["value"] = self.chat.send_message(prompt)

        t = threading.Thread(target=target)
        t.start()

        while t.is_alive() and not self.signal_queue.shutdown_is_set():
            t.join(timeout=0.3)  # wait in 1-second chunks

        if "value" not in response_holder:
            raise TimeoutError("Forced shutdown")

        response = response_holder["value"] #self.chat.send_message(prompt)
        text = response.text
        if code_only:
            return code.Code(text)
        else:
            return text
