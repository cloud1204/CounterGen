import utils.code as code
from utils.signal import Signal_Queue
import threading
from openai import OpenAI

class OpenAI_Agent:
    def __init__(self, signal_queue: Signal_Queue, API_KEY: str, model_type: str = "gpt-4o"):
        self.signal_queue = signal_queue
        self.client = OpenAI(api_key=API_KEY)
        self.model_type = model_type
        self.messages = []  # [{"role":"user"/"assistant","content": str}]

    def instruct(self, prompt, code_only=False):
        response_holder = {}

        def target():
            try:
                local_messages = self.messages + [{"role": "user", "content": prompt}]
                # Responses API accepts a list of role/content dicts as `input`
                response_holder["value"] = self.client.responses.create(
                    model=self.model_type,
                    input=local_messages,
                    max_output_tokens=1024
                )
            except Exception as e:
                response_holder["error"] = e

        t = threading.Thread(target=target)
        t.start()

        while t.is_alive() and not self.signal_queue.shutdown_is_set():
            t.join(timeout=0.3)  # wait in 0.3s chunks

        if "error" in response_holder:
            raise response_holder["error"]
        if "value" not in response_holder:
            raise TimeoutError("Forced shutdown")

        response = response_holder["value"]

        # Prefer the convenience accessor; fallback to manual join if needed
        text = ""
        try:
            text = getattr(response, "output_text", "") or ""
        except Exception:
            pass
        if not text:
            try:
                # Defensive: concatenate any text parts in output items
                parts = []
                for item in getattr(response, "output", []) or []:
                    if getattr(item, "type", None) == "output_text":
                        parts.append(getattr(item, "text", "") or "")
                text = "".join(parts)
            except Exception:
                text = ""

        # Update conversation history with the plain text we extracted
        self.messages.append({"role": "user", "content": prompt})
        self.messages.append({"role": "assistant", "content": text})

        return code.Code(text) if code_only else text
