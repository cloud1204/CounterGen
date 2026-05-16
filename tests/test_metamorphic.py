import unittest
from utils.code import Code
from scripts.validator import Validator
from scripts.metamorphic import Metamorphic, Metamorphic_Agent
from tests.fakes import FakeAgent


ALWAYS_VALID = "def validate(s):\n    return 'valid'\n"
ALWAYS_INVALID = "def validate(s):\n    return 'invalid: bad'\n"


def _validator(code_text=ALWAYS_VALID):
    return Validator(Code(code_text))


class MetamorphicLoadTests(unittest.TestCase):
    def test_loads_module_with_both_functions(self):
        module = (
            "def transform(s):\n    return s\n"
            "def relate(a, b, c, d):\n    return 'OK'\n"
        )
        m = Metamorphic(Code(module))
        self.assertEqual(m.transform("foo"), "foo")
        self.assertEqual(m.relate("a", "b", "c", "d"), "OK")

    def test_missing_transform_raises_valueerror(self):
        module = "def relate(a, b, c, d):\n    return 'OK'\n"
        with self.assertRaises(ValueError):
            Metamorphic(Code(module))

    def test_missing_relate_raises_valueerror(self):
        module = "def transform(s):\n    return s\n"
        with self.assertRaises(ValueError):
            Metamorphic(Code(module))


class MetamorphicAgentGenerateTests(unittest.TestCase):
    VALID_MODULE = (
        "```python\n"
        "def transform(s):\n    return s + 'x'\n"
        "def relate(a, b, c, d):\n    return 'OK'\n"
        "```"
    )

    def test_returns_none_when_llm_opts_out(self):
        agent = FakeAgent(["No"])
        ma = Metamorphic_Agent(agent, "stmt", "example", "out")
        self.assertIsNone(ma.generate(_validator()))
        # Should not have asked for the module after a "No".
        self.assertEqual(len(agent.received_prompts), 1)

    def test_returns_metamorphic_when_transform_validates(self):
        agent = FakeAgent(["Yes, append-x transform.", self.VALID_MODULE])
        ma = Metamorphic_Agent(agent, "stmt", "example", "out")
        m = ma.generate(_validator())
        self.assertIsNotNone(m)
        self.assertEqual(m.transform("foo"), "foox")
        self.assertEqual(m.relate("a", "b", "c", "d"), "OK")

    def test_skips_when_transform_never_validates(self):
        agent = FakeAgent([
            "Yes, identity",
            self.VALID_MODULE,  # transform output rejected by validator
            self.VALID_MODULE,
            self.VALID_MODULE,
            self.VALID_MODULE,
        ])
        ma = Metamorphic_Agent(agent, "stmt", "example", "out")
        self.assertIsNone(ma.generate(_validator(ALWAYS_INVALID)))

    def test_retries_when_module_fails_to_load(self):
        bad_module = (
            "```python\n"
            "def transform(s):\n    return s\n"
            "def relate(a, b, c, d):\n    return 'OK'\n"
            "stray = qwq\n"
            "```"
        )
        agent = FakeAgent([
            "Yes, fine",
            bad_module,           # initial module fails to load (NameError at exec)
        ])
        ma = Metamorphic_Agent(agent, "stmt", "example", "out")
        # Current generate() short-circuits to None on module load failure;
        # this test pins that behavior so a future refactor toward retry is intentional.
        self.assertIsNone(ma.generate(_validator()))


if __name__ == '__main__':
    unittest.main()
