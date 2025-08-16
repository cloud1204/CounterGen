import google.generativeai as genai
import utils.code as code
from utils.signal import Signal_Queue
import threading
class Gemini_Agent:
    def __init__(self, signal_queue: Signal_Queue, API_KEY: str, model_type : str ='2.5-flash'):
        self.signal_queue = signal_queue
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(model_type)
        self.chat = self.model.start_chat()
    def instruct(self, prompt, code_only = False):
        response_holder = {}
        def target():
            try:
                response_holder["value"] = self.chat.send_message(prompt)
            except Exception as e:
                response_holder["error"] = e

        t = threading.Thread(target=target)
        t.start()

        while t.is_alive() and not self.signal_queue.shutdown_is_set():
            t.join(timeout=0.3)  # wait in 1-second chunks

        if "error" in response_holder:
            raise response_holder["error"]
        if "value" not in response_holder:
            raise TimeoutError("Forced shutdown")

        response = response_holder["value"] #self.chat.send_message(prompt)
        text = response.text
        if code_only:
            return code.Code(text)
        else:
            return text
