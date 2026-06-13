from utils.agent import Agent
from utils.code import Code
from scripts.validator import Validator
import time


class Metamorphic:
    def __init__(self, module_code: Code):
        self.code = module_code.code
        self.namespace = {}
        exec(module_code.code, self.namespace)
        if 'transform' not in self.namespace or 'relate' not in self.namespace:
            raise ValueError("Metamorphic module must define both 'transform' and 'relate' functions.")
        self.transform = self.namespace['transform']
        self.relate = self.namespace['relate']


PROBE_PROMPT = """Does this problem admit a useful metamorphic relation -- an input transformation T \
and an output relation R such that for any valid input x with correct output y, applying T to get x' yields \
an output y' satisfying R(x, y, x', y') for ANY correct solution?

Examples that often work:
- Permutation invariance (shuffle an unordered collection -> same answer)
- Linear scaling (multiply all weights/values by k -> answer scales by k)
- Adding non-interfering elements (e.g. extra unreachable nodes, padding zeros)
- Duplicating a self-contained sub-instance (answer combines predictably)
- Relabeling/renaming anonymous elements

A useful relation does NOT need to be a strict equality -- a one-sided bound \
(answer can only stay the same or change in a known direction) is also fine, as long as \
you can state the bound precisely in `relate`.

Be careful with these traps -- prefer "No" if you suspect them:
- Output is a specific construction, index, position, or witness (any reordering changes it).
- "Lexicographically smallest/largest" answers where the tie-break depends on input order.
- The problem has a directional/order-sensitive operation (left-to-right scan, prefix DP, \
shift/rotation, turn-based game) AND your transformation reverses or reorders the input. \
Mirror / reverse-and-swap transformations are especially risky on such problems: they preserve \
high-level structural invariants but routinely break the actual count or value the problem asks for.

If a clean relation exists, reply:
  Yes. <one-sentence description of the relation>

If not, reply with exactly:
  No"""


MODULE_PROMPT = """Now give me a Python module containing exactly these two functions:

def transform(input_str: str) -> str:
    # Apply the metamorphic transformation; return a NEW valid input in the same format as the original.
    # May use the random module.

def relate(in1: str, out1: str, in2: str, out2: str) -> str:
    # in2 = transform(in1). out1 and out2 are outputs produced by a candidate solution.
    # Return 'OK' if (out1, out2) satisfies the expected relation under the transformation.
    # Otherwise return a short failure reason string.

Requirements:
- transform must always produce input that satisfies the problem's input constraints.
- relate must return 'OK' for ANY correct solution. A FALSE POSITIVE (reporting a failure on a correct \
solution) is much worse than reporting 'OK' too often. When uncertain, return 'OK'.
- relate must handle output-format variation gracefully: trailing whitespace, optional trailing newline, \
multiple valid answers, equivalent representations (e.g. different orderings of an unordered answer set). \
If the problem allows multiple correct outputs, do NOT compare them for equality -- only check the \
weaker invariant you actually proved.
- Do not insert any comments. Give the python code only."""


class Metamorphic_Agent:
    def __init__(self, agent: Agent, problem_statement: str, example_input: str, example_output: str):
        self.agent = agent
        self.problem_statement = problem_statement
        self.example_input = example_input
        self.example_output = example_output

    def generate(self, validator: Validator):
        start_time = time.time()
        probe = self.agent.instruct(f"{self.problem_statement}\n\n{PROBE_PROMPT}")
        if probe.strip().lower().startswith('no'):
            print("Metamorphic: no useful relation for this problem. Skipping metamorphic check.")
            return None
        first_line = probe.strip().splitlines()[0][:200] if probe.strip() else ""
        print(f"Metamorphic: relation chosen -- {first_line}")

        try:
            metamorphic = Metamorphic(self.agent.instruct(MODULE_PROMPT, code_only=True))
        except Exception as e:
            print(f"Metamorphic: module generation failed ({e}). Skipping.")
            return None

        MAX_TRY = 4
        for _ in range(MAX_TRY):
            try:
                transformed = metamorphic.transform(self.example_input)
            except Exception as e:
                print(f"Metamorphic: transform raised {e}. Regenerating.")
                prompt = (f"transform raised an exception on the example input:\n{e}\n"
                          f"Give me the corrected module (both transform and relate). Do not insert any comments.")
                try:
                    metamorphic = Metamorphic(self.agent.instruct(prompt, code_only=True))
                except Exception as ee:
                    print(f"Metamorphic: regeneration failed ({ee}). Skipping.")
                    return None
                continue

            if not isinstance(transformed, str):
                print(f"Metamorphic: transform returned non-string ({type(transformed).__name__}). Regenerating.")
                prompt = ("transform must return a string. Give me the corrected module. "
                          "Do not insert any comments.")
                try:
                    metamorphic = Metamorphic(self.agent.instruct(prompt, code_only=True))
                except Exception as ee:
                    print(f"Metamorphic: regeneration failed ({ee}). Skipping.")
                    return None
                continue

            v = validator.validate(transformed).strip()
            if v != 'valid':
                print(f"Metamorphic: transform produced invalid input ({v}). Regenerating.")
                prompt = (f"The transform produced an input that the validator rejected.\n"
                          f"Validator said: {v}\nGenerated input was:\n{transformed}\n"
                          f"Give me the corrected module (both transform and relate). Do not insert any comments.")
                try:
                    metamorphic = Metamorphic(self.agent.instruct(prompt, code_only=True))
                except Exception as ee:
                    print(f"Metamorphic: regeneration failed ({ee}). Skipping.")
                    return None
                continue

            print(f"Metamorphic relation ready. Time spent: {time.time() - start_time:.2f} sec")
            return metamorphic

        print("Metamorphic: transform never produced valid input after retries. Skipping.")
        return None
