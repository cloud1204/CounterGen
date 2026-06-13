import utils.code as code
from utils.signal import Signal_Queue
from utils import usage
import threading
import anthropic

# Anthropic prices, USD per 1M tokens (input, output), matched by substring against
# the model id. Anthropic's API does not return a cost, so these drive the
# per-problem cost cap and the usage report. An unknown model yields cost 0 (the cap
# then never fires).
#
# opus: CALIBRATED to observed claude-opus-4-7 billing (2026-06): $13.09 for
# 255,262 in + 472,576 out tokens -> $5 / $25 per MTok, exactly 1/3 of the $15/$75
# list price (a discount/promo or caching effect). Re-check if you use a different
# Opus model or your effective rate changes. sonnet/haiku are list prices (uncalibrated).
_CLAUDE_PRICES = [
    ("opus", (5.0, 25.0)),
    ("sonnet", (3.0, 15.0)),
    ("haiku", (1.0, 5.0)),
]


def _model_prices(model):
    """(input, output) USD/MTok for a model id, or (0, 0) if unknown."""
    m = (model or "").lower()
    for key, prices in _CLAUDE_PRICES:
        if key in m:
            return prices
    return 0.0, 0.0


def _estimate_cost(model, input_tokens, output_tokens):
    p_in, p_out = _model_prices(model)
    return input_tokens / 1e6 * p_in + output_tokens / 1e6 * p_out


def _projected_call_cost(model, messages, prompt, max_tokens):
    """Worst-case cost of one call BEFORE sending: estimated input tokens (~4
    chars/token over the conversation + prompt) plus the full max_tokens of
    output. Used to refuse a call that would blow the per-call cap."""
    p_in, p_out = _model_prices(model)
    chars = sum(len(m.get("content", "")) for m in messages) + len(prompt or "")
    est_input_tokens = chars / 4
    return est_input_tokens / 1e6 * p_in + max_tokens / 1e6 * p_out


class Claude_Agent:
    def __init__(self, signal_queue: Signal_Queue, API_KEY: str, model_type: str = 'default',
                 max_tokens: int = 8192):
        self.signal_queue = signal_queue
        self.client = anthropic.Anthropic(api_key=API_KEY)
        self.model_type = model_type
        self.max_tokens = max_tokens  # 1024 was too low -- it truncated generated code
        self.messages = []

    def instruct(self, prompt, code_only = False):
        if usage.over_budget():
            raise RuntimeError("per-problem API cost cap reached; skipping further LLM calls")
        cap = usage.call_cap()
        if cap is not None:
            projected = _projected_call_cost(self.model_type, self.messages, prompt, self.max_tokens)
            if projected > cap:
                raise RuntimeError(
                    f"projected single-call cost ~${projected:.2f} exceeds per-call cap "
                    f"${cap:.2f}; skipping (input too large)")
        response_holder = {}
        def target():
            try:
                local_messages = self.messages + [{"role": "user", "content": prompt}]
                response_holder["value"] = self.client.messages.create(
                    model=self.model_type,
                    max_tokens=self.max_tokens,
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

        try:
            u = getattr(response, "usage", None)
            if u is not None:
                it = getattr(u, "input_tokens", 0) or 0
                ot = getattr(u, "output_tokens", 0) or 0
                usage.record(prompt_tokens=it, completion_tokens=ot, total_tokens=it + ot,
                             cost=_estimate_cost(self.model_type, it, ot))
        except Exception:
            pass

        self.messages.append({"role": "user", "content": prompt})
        self.messages.append({"role": "assistant", "content": text})

        if code_only:
            return code.Code(text)
        else:
            return text
