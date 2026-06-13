"""Process-global LLM API usage accumulator.

Provider agents call record() after each API call; callers reset() before a unit
of work and snapshot() after to read what that unit consumed. Thread-safe, so it
works under the benchmark's parallel generation; process-global, so under the
benchmark's per-problem process isolation each problem naturally gets its own
tally with no plumbing.

Only providers that call record() contribute (OpenRouter and Claude are wired;
Claude's cost is estimated from a price table since its API returns no cost). For
other providers the snapshot is simply zero -- never wrong, just unpopulated.
"""
import threading

_lock = threading.Lock()
_totals = {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0,
           'total_tokens': 0, 'cost': 0.0}
_budget = None  # cumulative USD cap for the current unit of work; None = no cap
_call_cap = None  # per-single-call USD ceiling; None = no cap


def record(prompt_tokens=0, completion_tokens=0, total_tokens=0, cost=0.0):
    with _lock:
        _totals['calls'] += 1
        _totals['prompt_tokens'] += int(prompt_tokens or 0)
        _totals['completion_tokens'] += int(completion_tokens or 0)
        _totals['total_tokens'] += int(total_tokens or 0)
        _totals['cost'] += float(cost or 0.0)


def reset():
    """Clear accumulated usage. Does NOT clear the budget (set per run)."""
    with _lock:
        for k in _totals:
            _totals[k] = 0 if k != 'cost' else 0.0


def snapshot():
    with _lock:
        return dict(_totals)


def set_budget(cost_limit):
    """Set the USD cost cap for the current unit of work (None disables it).

    The cap only fires for providers that report per-call cost (OpenRouter does);
    others report cost 0, so over_budget() stays False and there is no cap."""
    global _budget
    with _lock:
        _budget = cost_limit


def over_budget():
    """True once accumulated cost has reached the budget. Checked at the top of
    each API call so a single problem can't keep spending past the cap (overshoot
    is bounded by the calls already in flight when the line is crossed)."""
    with _lock:
        return _budget is not None and _totals['cost'] >= _budget


def set_call_cap(cost_limit):
    """Set a per-single-call USD ceiling (None disables it). A provider agent
    estimates a call's worst-case cost BEFORE sending and refuses it if it would
    exceed this -- a guard against one runaway call (e.g. a huge output) even when
    the cumulative budget still has room."""
    global _call_cap
    with _lock:
        _call_cap = cost_limit


def call_cap():
    with _lock:
        return _call_cap
