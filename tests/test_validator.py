import unittest
from utils.code import Code
from scripts.validator import Validator, TC_Validator_Agent
from tests.fakes import FakeAgent


class ValidatorLoadTests(unittest.TestCase):
    def test_valid_code_loads_and_runs(self):
        v = Validator(Code("def validate(s):\n    return 'valid'\n"))
        self.assertEqual(v.validate("anything").strip(), 'valid')

    def test_top_level_name_error_raises_valueerror(self):
        # Mirrors the qwq bug: LLM left a top-level statement referencing an undefined name.
        code = Code("def validate(s):\n    return 'valid'\n\nresult = validate(qwq)\n")
        with self.assertRaises(ValueError):
            Validator(code)

    def test_missing_validate_function_raises_valueerror(self):
        code = Code("def something_else(s):\n    return 'valid'\n")
        with self.assertRaises(ValueError):
            Validator(code)

    def test_non_callable_validate_raises_valueerror(self):
        code = Code("validate = 42\n")
        with self.assertRaises(ValueError):
            Validator(code)


class TCValidatorAgentMakeValidatorTests(unittest.TestCase):
    BAD_RESPONSE = "```python\ndef validate(s):\n    return 'valid'\n\nx = qwq\n```"
    GOOD_RESPONSE = "```python\ndef validate(s):\n    return 'valid'\n```"

    def test_retries_when_load_fails_then_succeeds(self):
        agent = FakeAgent([self.BAD_RESPONSE, self.GOOD_RESPONSE])
        tca = TC_Validator_Agent(agent, "stmt", "ex_in", "ex_out")
        v = tca._make_validator("initial prompt")
        self.assertEqual(v.validate("any").strip(), 'valid')
        self.assertEqual(len(agent.received_prompts), 2)
        self.assertIn("could not be loaded", agent.received_prompts[1])
        self.assertIn("ONLY the", agent.received_prompts[1])

    def test_raises_runtime_error_after_three_failures(self):
        agent = FakeAgent([self.BAD_RESPONSE, self.BAD_RESPONSE, self.BAD_RESPONSE])
        tca = TC_Validator_Agent(agent, "stmt", "ex_in", "ex_out")
        with self.assertRaises(RuntimeError):
            tca._make_validator("initial prompt")
        self.assertEqual(len(agent.received_prompts), 3)

    def test_parse_failure_also_triggers_retry(self):
        # LLM response that contains backticks but malformed Python inside.
        garbage = "```\ndef (:\n```"
        agent = FakeAgent([garbage, self.GOOD_RESPONSE])
        tca = TC_Validator_Agent(agent, "stmt", "ex_in", "ex_out")
        v = tca._make_validator("initial prompt")
        self.assertEqual(v.validate("any").strip(), 'valid')


class TCValidatorAgentWorkTests(unittest.TestCase):
    GOOD_RESPONSE = "```python\ndef validate(s):\n    return 'valid'\n```"
    ALWAYS_INVALID = "```python\ndef validate(s):\n    return 'invalid: nope'\n```"

    def test_work_returns_validator_on_first_success(self):
        agent = FakeAgent([self.GOOD_RESPONSE])
        tca = TC_Validator_Agent(agent, "stmt", "ex_in", "ex_out")
        v = tca.work()
        self.assertEqual(v.validate("any").strip(), 'valid')

    def test_work_regenerates_when_validator_rejects_example(self):
        agent = FakeAgent([self.ALWAYS_INVALID, self.GOOD_RESPONSE])
        tca = TC_Validator_Agent(agent, "stmt", "ex_in", "ex_out")
        v = tca.work()
        self.assertEqual(v.validate("any").strip(), 'valid')

    def test_work_raises_when_never_accepts_example(self):
        agent = FakeAgent([self.ALWAYS_INVALID] * 10)
        tca = TC_Validator_Agent(agent, "stmt", "ex_in", "ex_out")
        with self.assertRaises(RuntimeError):
            tca.work()


if __name__ == '__main__':
    unittest.main()
