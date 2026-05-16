import unittest
from scripts.AC_generator import AC_Agent
from tests.fakes import FakeAgent, FakeCode, FakeRunResult


class StubMetamorphic:
    def __init__(self, transform_fn, relate_fn):
        self.transform = transform_fn
        self.relate = relate_fn


def _make_ac_agent(ac_code, metamorphic, example_input="EX_IN"):
    agent = FakeAgent([])  # _metamorphic_check should not call the LLM
    a = AC_Agent(agent, "stmt", example_input, "EX_OUT")
    a.AC_code = ac_code
    a.set_metamorphic(metamorphic)
    return a


class MetamorphicCheckTests(unittest.TestCase):
    def test_returns_none_when_no_metamorphic(self):
        a = _make_ac_agent(ac_code=FakeCode({}), metamorphic=None)
        self.assertIsNone(a._metamorphic_check("any output"))

    def test_returns_none_when_relate_says_ok(self):
        ac = FakeCode({"EX_IN_t": "transformed_out"})
        meta = StubMetamorphic(
            transform_fn=lambda s: s + "_t",
            relate_fn=lambda i1, o1, i2, o2: "OK",
        )
        a = _make_ac_agent(ac, meta)
        self.assertIsNone(a._metamorphic_check("original_out"))

    def test_returns_reason_when_relate_fails(self):
        ac = FakeCode({"EX_IN_t": "wrong_out"})
        meta = StubMetamorphic(
            transform_fn=lambda s: s + "_t",
            relate_fn=lambda i1, o1, i2, o2: "expected X, got Y",
        )
        a = _make_ac_agent(ac, meta)
        reason = a._metamorphic_check("original_out")
        self.assertIsNotNone(reason)
        self.assertIn("expected X, got Y", reason)
        self.assertIn("EX_IN_t", reason)

    def test_returns_none_when_transform_raises(self):
        def boom(_):
            raise RuntimeError("transform exploded")
        meta = StubMetamorphic(transform_fn=boom, relate_fn=lambda *a: "OK")
        a = _make_ac_agent(FakeCode({}), meta)
        # Defensive: a buggy transform should not block AC acceptance.
        self.assertIsNone(a._metamorphic_check("orig"))

    def test_returns_reason_when_ac_crashes_on_transformed_input(self):
        ac = FakeCode({"EX_IN_t": FakeRunResult(stdout="", stderr="boom", returncode=1)})
        meta = StubMetamorphic(
            transform_fn=lambda s: s + "_t",
            relate_fn=lambda *a: "OK",
        )
        a = _make_ac_agent(ac, meta)
        reason = a._metamorphic_check("orig")
        self.assertIsNotNone(reason)
        self.assertIn("crashed", reason)

    def test_returns_reason_when_ac_times_out_on_transformed_input(self):
        ac = FakeCode({"EX_IN_t": "timeout"})
        meta = StubMetamorphic(
            transform_fn=lambda s: s + "_t",
            relate_fn=lambda *a: "OK",
        )
        a = _make_ac_agent(ac, meta)
        reason = a._metamorphic_check("orig")
        self.assertIsNotNone(reason)
        self.assertIn("timed out", reason)


if __name__ == '__main__':
    unittest.main()
