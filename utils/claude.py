import utils.code as code
from utils.signal import Signal_Queue
import threading
import anthropic
class Claude_Agent:
    def __init__(self, signal_queue: Signal_Queue, API_KEY: str, model_type : str ='default'):
        self.signal_queue = signal_queue
        self.client = anthropic.Anthropic(api_key=API_KEY)
        self.model_type = model_type
        self.messages = []
    def instruct(self, prompt, code_only = False):
        response_holder = {}
        def target():
            try:
                local_messages = self.messages + [{"role": "user", "content": prompt}]
                response_holder["value"] = self.client.messages.create(
                    model=self.model_type,
                    max_tokens=1024,
                    messages=local_messages
                )
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

        response = response_holder["value"]
        text = ''
        if hasattr(response, "content") and response.content:
            try:
                text = "".join([part.text for part in response.content if getattr(part, "type", None) == "text"])
            except Exception:
                pass
        
        self.messages.append({"role": "user", "content": prompt})
        self.messages.append({"role": "assistant", "content": text})

        if code_only:
            return code.Code(text)
        else:
            return text
