import utils.code as code
from utils.signal import Signal_Queue
import threading
from openai import OpenAI


class OpenRouter_Agent:
    def __init__(self, signal_queue: Signal_Queue, API_KEY: str,
                 model_type: str = "google/gemini-2.5-flash"):
        self.signal_queue = signal_queue
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )
        self.model_type = model_type
        self.messages = []

    def instruct(self, prompt, code_only=False):
        response_holder = {}

        def target():
            try:
                local_messages = self.messages + [{"role": "user", "content": prompt}]
                response = self.client.chat.completions.create(
                    model=self.model_type,
                    messages=local_messages,
                    extra_headers={
                        "HTTP-Referer": "https://github.com/cloud1204/CounterGen",
                        "X-Title": "CounterGen",
                    },
                )
                response_holder["value"] = response.choices[0].message.content
            except Exception as e:
                response_holder["error"] = e

        t = threading.Thread(target=target)
        t.start()

        while t.is_alive() and not self.signal_queue.shutdown_is_set():
            t.join(timeout=0.3)

        if "error" in response_holder:
            raise response_holder["error"]
        if "value" not in response_holder:
            raise TimeoutError("Forced shutdown")

        text = response_holder["value"]

        self.messages.append({"role": "user", "content": prompt})
        self.messages.append({"role": "assistant", "content": text})

        return code.Code(text) if code_only else text
