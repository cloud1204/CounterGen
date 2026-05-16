"""
Integration test for Metamorphic_Agent.

Tests whether the LLM-generated metamorphic relation can actually distinguish
correct from buggy solutions on a few hand-picked problems.

Unlike the unit tests, this hits a real LLM API, so results are non-deterministic.
The script is named 'integration_*' (not 'test_*') so `unittest discover` skips it.

Run with:
    .venv/Scripts/python.exe -m tests.integration_metamorphic

Credentials are read from Input_Cache/settings.yaml (whatever provider Last_Use points
to) or from one of these env vars: GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY.
"""

import os
import sys
import yaml

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from utils.code import Code
from utils.agent import Agent
from utils.signal import Signal_Queue
from scripts.validator import TC_Validator_Agent
from scripts.metamorphic import Metamorphic_Agent
from scripts.AC_generator import AC_Agent


CASES = [
    {
        "name": "Sum of array (wrong: drops last element)",
        "statement": (
            "You are given n integers a_1, a_2, ..., a_n on two lines: the first "
            "line contains n (1 <= n <= 100), the second line contains the n "
            "integers separated by spaces (1 <= a_i <= 1000). Output their sum on "
            "a single line."
        ),
        "example_in": "5\n1 2 3 4 5\n",
        "example_out": "15\n",
        "correct": (
            "n = int(input())\n"
            "print(sum(map(int, input().split())))\n"
        ),
        "wrong": (
            "n = int(input())\n"
            "a = list(map(int, input().split()))\n"
            "print(sum(a[:-1]))\n"
        ),
    },
    {
        "name": "Median (wrong: assumes input is sorted)",
        "statement": (
            "You are given n integers on two lines: the first line contains an odd "
            "integer n (1 <= n <= 99), the second line contains the n integers "
            "separated by spaces (1 <= a_i <= 1000). Output their median."
        ),
        "example_in": "5\n1 2 3 4 5\n",
        "example_out": "3\n",
        "correct": (
            "n = int(input())\n"
            "a = sorted(map(int, input().split()))\n"
            "print(a[n // 2])\n"
        ),
        "wrong": (
            "n = int(input())\n"
            "a = list(map(int, input().split()))\n"
            "print(a[n // 2])\n"
        ),
    },
]


PROVIDER_ENV_VARS = {
    "Gemini": "GEMINI_API_KEY",
    "Claude": "ANTHROPIC_API_KEY",
    "OpenAI": "OPENAI_API_KEY",
    "OpenRouter": "OPENROUTER_API_KEY",
}

PROVIDER_DEFAULT_MODELS = {
    "Gemini": "gemini-2.5-flash",
    "Claude": "claude-sonnet-4-0",
    "OpenAI": "gpt-4o",
    "OpenRouter": "google/gemini-2.5-flash",
    "vLLM": "Qwen/Qwen2.5-Coder-14B-Instruct-AWQ",
}


def _resolve_provider(provider, settings_data):
    """Look up (api_key, model_from_settings) for one provider."""
    cfg = settings_data.get(provider) or {}
    key = cfg.get("API_KEY")
    model = cfg.get("AC") or cfg.get("val/gen")
    if not key or key == "not needed":
        env = PROVIDER_ENV_VARS.get(provider)
        if env:
            key = os.environ.get(env) or key
    if provider == "vLLM":
        key = "not needed"
    return key, model


def load_credentials(provider_override=None, model_override=None):
    """
    Returns (provider, api_key, model).

    Resolution order:
      - if provider_override: look up that provider's key (settings.yaml then env var).
      - else: settings.yaml's Last_Use, then env vars (OpenRouter, Gemini, Claude, OpenAI).
      - model_override always wins; otherwise model comes from settings AC field or
        a built-in default per provider. OpenRouter additionally honors OPENROUTER_MODEL.
    """
    settings_path = os.path.join(_HERE, "..", "Input_Cache", "settings.yaml")
    settings_data = {}
    if os.path.exists(settings_path):
        with open(settings_path) as f:
            settings_data = yaml.safe_load(f) or {}

    def _default_model(provider):
        if provider == "OpenRouter":
            return os.environ.get("OPENROUTER_MODEL") or PROVIDER_DEFAULT_MODELS[provider]
        return PROVIDER_DEFAULT_MODELS.get(provider)

    def _is_valid_key(key, provider):
        if provider == "vLLM":
            return True
        return bool(key) and key != "not needed"

    if provider_override:
        key, model = _resolve_provider(provider_override, settings_data)
        if not _is_valid_key(key, provider_override):
            return None, None, None
        return provider_override, key, (model_override or model or _default_model(provider_override))

    last_use = settings_data.get("Last_Use")
    if last_use:
        key, model = _resolve_provider(last_use, settings_data)
        if _is_valid_key(key, last_use):
            return last_use, key, (model_override or model or _default_model(last_use))

    for provider in ["OpenRouter", "Gemini", "Claude", "OpenAI"]:
        env = PROVIDER_ENV_VARS[provider]
        if os.environ.get(env):
            return provider, os.environ[env], (model_override or _default_model(provider))

    return None, None, None


def _run_one(label, code_text, case, meta, agent):
    print(f"  [{label}]")
    try:
        code = Code(code_text)
    except Exception as e:
        print(f"    code did not compile: {e}")
        return "compile-failed"
    ac_agent = AC_Agent(agent, case["statement"], case["example_in"], case["example_out"])
    ac_agent.AC_code = code
    ac_agent.set_metamorphic(meta)
    run = code.execute(case["example_in"])
    if run == "timeout":
        print("    timed out on example input")
        return "timeout"
    if getattr(run, "stderr", "") or getattr(run, "returncode", 0) != 0:
        print(f"    crashed on example: {getattr(run, 'stderr', '')}")
        return "crashed"
    reason = ac_agent._metamorphic_check(run.stdout)
    if reason is None:
        print("    -> passed metamorphic check")
        return "pass"
    short = reason if len(reason) <= 400 else reason[:400] + " ..."
    print(f"    -> FAILED metamorphic check:\n      {short}")
    return "fail"


def run_case(case, provider, api_key, model):
    print("\n" + "=" * 72)
    print(f"CASE: {case['name']}")
    print("=" * 72)

    sq = Signal_Queue()

    print("Generating validator ...")
    try:
        val_agent = Agent(sq, provider, api_key, model, "Validator")
        validator = TC_Validator_Agent(
            val_agent, case["statement"], case["example_in"], case["example_out"]
        ).work()
    except Exception as e:
        print(f"  validator generation failed: {e}")
        return {"correct": "validator-failed", "wrong": "validator-failed"}

    print("Generating metamorphic relation ...")
    try:
        meta_agent = Agent(sq, provider, api_key, model, "Metamorphic")
        meta = Metamorphic_Agent(
            meta_agent, case["statement"], case["example_in"], case["example_out"]
        ).generate(validator)
    except Exception as e:
        print(f"  metamorphic generation failed: {e}")
        return {"correct": "meta-failed", "wrong": "meta-failed"}

    if meta is None:
        print("  LLM declined to provide a metamorphic relation; nothing to test.")
        return {"correct": "declined", "wrong": "declined"}

    correct_verdict = _run_one("CORRECT", case["correct"], case, meta, meta_agent)
    wrong_verdict = _run_one("WRONG  ", case["wrong"], case, meta, meta_agent)
    return {"correct": correct_verdict, "wrong": wrong_verdict}


def summarize(results):
    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    headers = f"  {'case':<55} {'correct':<14} {'wrong':<14}"
    print(headers)
    print("  " + "-" * (len(headers) - 2))
    for name, r in results:
        c, w = r["correct"], r["wrong"]
        c_tag = c
        w_tag = w
        if c == "pass":
            c_tag = "pass (good)"
        elif c == "fail":
            c_tag = "FALSE POSITIVE"
        if w == "fail":
            w_tag = "caught (good)"
        elif w == "pass":
            w_tag = "FALSE NEGATIVE"
        truncated = name if len(name) <= 53 else name[:50] + "..."
        print(f"  {truncated:<55} {c_tag:<14} {w_tag:<14}")


def main():
    provider, api_key, model = load_credentials()
    if not api_key:
        print("No API key found.")
        print("  Run UI.py once and enter your key (cached in Input_Cache/settings.yaml), or")
        print("  set GEMINI_API_KEY / ANTHROPIC_API_KEY / OPENAI_API_KEY.")
        return 1
    print(f"Using provider={provider}, model={model}")

    results = []
    for case in CASES:
        try:
            results.append((case["name"], run_case(case, provider, api_key, model)))
        except Exception as e:
            import traceback
            traceback.print_exc()
            results.append((case["name"], {"correct": "error", "wrong": "error"}))

    summarize(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
