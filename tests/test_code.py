import unittest
from utils.code import Code


class CodeExtractionTests(unittest.TestCase):
    def test_raw_python_code_accepted_as_is(self):
        c = Code("def f():\n    return 1\n")
        self.assertEqual(c.language, 'python')
        self.assertIn("def f():", c.code)

    def test_python_block_with_language_tag(self):
        text = "Sure, here you go:\n```python\ndef g():\n    return 2\n```\nLet me know!"
        c = Code(text)
        self.assertEqual(c.language, 'python')
        self.assertIn("def g():", c.code)
        self.assertNotIn("python\n", c.code)

    def test_python_block_with_py_tag(self):
        text = "```py\ndef h():\n    return 3\n```"
        c = Code(text)
        self.assertIn("def h():", c.code)
        self.assertNotIn("py\n", c.code.splitlines()[0])

    def test_python_block_without_language_tag(self):
        text = "```\ndef k():\n    return 4\n```"
        c = Code(text)
        self.assertIn("def k():", c.code)

    def test_skips_invalid_first_block_picks_valid_second(self):
        text = "```\ndef (:\n```\n```python\ndef ok():\n    pass\n```"
        c = Code(text)
        self.assertIn("def ok():", c.code)
        self.assertNotIn("def (:", c.code)

    def test_raises_valueerror_when_no_code_blocks(self):
        with self.assertRaises(ValueError):
            Code("There is no code here, just text. ")

    def test_raises_valueerror_when_all_blocks_invalid(self):
        with self.assertRaises(ValueError):
            Code("```\ndef (:\n```")

    def test_does_not_raise_assertion_error_on_bad_block(self):
        # The pre-fix behavior used `assert is_valid_python_code(...)` which raised
        # AssertionError; callers expect ValueError so they can retry.
        try:
            Code("```\nnot python at all !!\n```")
        except ValueError:
            pass
        except AssertionError:
            self.fail("Code raised AssertionError; should raise ValueError instead.")


if __name__ == '__main__':
    unittest.main()
