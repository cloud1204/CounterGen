from utils.code import Code


class FakeAgent:
    def __init__(self, responses):
        self.responses = list(responses)
        self.received_prompts = []

    def instruct(self, prompt, code_only=False):
        self.received_prompts.append(prompt)
        if not self.responses:
            raise RuntimeError(f"FakeAgent ran out of scripted responses (received {len(self.received_prompts)} prompts).")
        text = self.responses.pop(0)
        if code_only:
            return Code(text)
        return text


class FakeRunResult:
    def __init__(self, stdout='', stderr='', returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


class FakeCode:
    def __init__(self, outputs):
        self.outputs = dict(outputs)
        self.calls = []

    def execute(self, input='', args=None, timeout=30):
        self.calls.append(input)
        if input not in self.outputs:
            raise RuntimeError(f"FakeCode: no scripted output for input={input!r}")
        resp = self.outputs[input]
        if resp == 'timeout':
            return 'timeout'
        if isinstance(resp, FakeRunResult):
            return resp
        return FakeRunResult(stdout=resp)
