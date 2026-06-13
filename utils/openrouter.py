import utils.code as code
from utils.signal import Signal_Queue
from utils import usage
import threading
from openai import OpenAI


def _usage_field(u, name, default=0):
    """Read a field from an OpenAI/OpenRouter usage object, tolerating both
    attribute access and pydantic 'extra' fields (OpenRouter adds `cost`)."""
    if u is None:
        return default
    v = getattr(u, name, None)
    if v is None:
        extra = getattr(u, 'model_extra', None)
        if isinstance(extra, dict):
            v = extra.get(name)
    if v is None and isinstance(u, dict):
        v = u.get(name)
    return v if v is not None else default


class OpenRouter_Agent:
    def __init__(self, signal_queue: Signal_Queue, API_KEY: str,
                 model_type: str = "google/gemini-2.5-flash", max_tokens: int = 8192):
        self.signal_queue = signal_queue
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=API_KEY,
        )
        self.model_type = model_type
        # Bound output per call. Left unset before, it defaulted huge (up to 65536),
        # which let a single call's output cost balloon -- the main cause of the
        # earlier $6 problem. OpenRouter returns real per-call cost, so the cumulative
        # cap still applies; this just caps any one call's output.
        self.max_tokens = max_tokens
        self.messages = []

    def instruct(self, prompt, code_only=False):
        if usage.over_budget():
            raise RuntimeError("per-problem API cost cap reached; skipping further LLM calls")
        response_holder = {}

        def target():
            try:
                local_messages = self.messages + [{"role": "user", "content": prompt}]
                response = self.client.chat.completions.create(
                    model=self.model_type,
                    messages=local_messages,
                    max_tokens=self.max_tokens,
                    extra_headers={
                        "HTTP-Referer": "https://github.com/cloud1204/CounterGen",
                        "X-Title": "CounterGen",
                    },
                    extra_body={"usage": {"include": True}},
                )
                response_holder["value"] = response.choices[0].message.content
                response_holder["usage"] = getattr(response, "usage", None)
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

        u = response_holder.get("usage")
        if u is not None:
            try:
                usage.record(
                    prompt_tokens=_usage_field(u, "prompt_tokens", 0),
                    completion_tokens=_usage_field(u, "completion_tokens", 0),
                    total_tokens=_usage_field(u, "total_tokens", 0),
                    cost=_usage_field(u, "cost", 0.0),
                )
            except Exception:
                pass

        self.messages.append({"role": "user", "content": prompt})
        self.messages.append({"role": "assistant", "content": text})

        return code.Code(text) if code_only else text
