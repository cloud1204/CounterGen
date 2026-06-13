"""Unit tests for experiment B (golden eval) and the per-relation metrics added
to tests/benchmark_metamorphic.py. Pure decision logic with fakes -- no LLM
calls, no real subprocesses."""
import time
import unittest

from scripts.checker import Checker, check_match
from tests.fakes import FakeCode, FakeRunResult
from tests import benchmark_metamorphic as bm


def _checker(func=check_match):
    c = Checker()
    c.checker_func = func
    return c


def _gp_golden(gt, example_verdicts=None, samples_verdicts=None):
    """A gate-pass golden corpus record with the given ground truth and verdict
    lists (one entry per relation)."""
    return {
        'index': 0, 'gate': 'pass', 'ground_truth': gt,
        'meta_example_verdicts': list(example_verdicts or []),
        'meta_samples_verdicts': list(samples_verdicts or []),
    }


def _problem_with_corpus(corpus):
    return {'problem': 'Codeforces_Data/difficulty_2000/9_X', 'status': 'ok',
            'goldens': {'num_goldens': len(corpus),
                        'gate_passed': sum(1 for g in corpus if g.get('gate') == 'pass'),
                        'corpus': corpus}}


class MetaVerdictTests(unittest.TestCase):
    def test_caught_is_flag(self):
        self.assertEqual(bm._meta_verdict({'status': 'caught'}), 'flag')

    def test_crash_statuses_are_flag(self):
        for s in ('exec-error', 'exec-timeout', 'compile-error'):
            self.assertEqual(bm._meta_verdict({'status': s}), 'flag')

    def test_pass_is_pass(self):
        self.assertEqual(bm._meta_verdict({'status': 'pass'}), 'pass')

    def test_unknown_status_is_na(self):
        self.assertEqual(bm._meta_verdict({'status': 'test-error'}), 'na')
        self.assertEqual(bm._meta_verdict({}), 'na')


class ExistingGateTests(unittest.TestCase):
    def test_pass_when_output_matches(self):
        ok, reason = bm._existing_gate(FakeCode({"EX_IN": "42\n"}), "EX_IN", "42\n", _checker())
        self.assertTrue(ok)
        self.assertEqual(reason, 'pass')

    def test_fail_on_wrong_example_output(self):
        ok, reason = bm._existing_gate(FakeCode({"EX_IN": "99\n"}), "EX_IN", "42\n", _checker())
        self.assertFalse(ok)
        self.assertIn('example WA', reason)

    def test_fail_on_crash(self):
        code = FakeCode({"EX_IN": FakeRunResult(stdout="", stderr="boom", returncode=1)})
        ok, reason = bm._existing_gate(code, "EX_IN", "42\n", _checker())
        self.assertFalse(ok)
        self.assertIn('exec-error', reason)

    def test_fail_on_timeout(self):
        ok, reason = bm._existing_gate(FakeCode({"EX_IN": "timeout"}), "EX_IN", "42\n", _checker())
        self.assertFalse(ok)
        self.assertIn('timeout', reason)


class CompareOnInputTests(unittest.TestCase):
    def test_agree(self):
        v, _ = bm._compare_on_input(FakeCode({"IN": "5\n"}), FakeCode({"IN": "5\n"}), _checker(), "IN")
        self.assertEqual(v, 'agree')

    def test_mismatch_when_checker_rejects(self):
        v, reason = bm._compare_on_input(FakeCode({"IN": "5\n"}), FakeCode({"IN": "6\n"}), _checker(), "IN")
        self.assertEqual(v, 'mismatch')
        self.assertIn('mismatch', reason)

    def test_crash_verdict(self):
        golden = FakeCode({"IN": FakeRunResult(stdout="", stderr="err", returncode=1)})
        v, reason = bm._compare_on_input(golden, FakeCode({"IN": "6\n"}), _checker(), "IN")
        self.assertEqual(v, 'crash')
        self.assertIn('crashed', reason)

    def test_tle_verdict(self):
        v, reason = bm._compare_on_input(FakeCode({"IN": "timeout"}), FakeCode({"IN": "6\n"}), _checker(), "IN")
        self.assertEqual(v, 'tle')
        self.assertIn('timed out', reason)

    def test_skip_when_reference_fails(self):
        v, _ = bm._compare_on_input(FakeCode({"IN": "5\n"}), FakeCode({"IN": "timeout"}), _checker(), "IN")
        self.assertEqual(v, 'skip')

    def test_reference_is_treated_as_correct_side(self):
        def only_ref_correct(_inp, out_a, out_b):
            return 'AC' if out_b == 'REF\n' else 'mismatch'
        v, _ = bm._compare_on_input(FakeCode({"IN": "X\n"}), FakeCode({"IN": "REF\n"}),
                                    _checker(only_ref_correct), "IN")
        self.assertEqual(v, 'agree')


class LabelGoldenTests(unittest.TestCase):
    def test_wrong_answer_on_example_short_circuits(self):
        label, witness = bm._label_golden(FakeCode({"EX": "1\n"}), FakeCode({"EX": "2\n"}),
                                          None, None, None, _checker(), "EX", 0)
        self.assertEqual(label, 'wrong-answer')
        self.assertIn('example input', witness)

    def test_correct_when_example_agrees_and_no_generator(self):
        label, _ = bm._label_golden(FakeCode({"EX": "1\n"}), FakeCode({"EX": "1\n"}),
                                    None, None, None, _checker(), "EX", 0)
        self.assertEqual(label, 'correct')

    def test_unknown_when_reference_fails_and_no_generator(self):
        label, _ = bm._label_golden(FakeCode({"EX": "1\n"}), FakeCode({"EX": "timeout"}),
                                    None, None, None, _checker(), "EX", 0)
        self.assertEqual(label, 'unknown')

    def test_wrong_answer_found_via_generator_input(self):
        golden = FakeCode({"EX": "1\n", "GEN": "5\n"})
        ref = FakeCode({"EX": "1\n", "GEN": "6\n"})
        orig = bm._sample_random_input
        bm._sample_random_input = lambda *a, **k: "GEN"
        try:
            label, witness = bm._label_golden(golden, ref, object(), [(1, 1)], object(),
                                              _checker(), "EX", 3)
        finally:
            bm._sample_random_input = orig
        self.assertEqual(label, 'wrong-answer')
        self.assertIn('GEN', witness)

    def test_tle_at_full_size_then_agree_when_shrunk_is_slow(self):
        # Golden agrees on the example, times out on the big generated input, but
        # AGREES on the shrunk input -> correct-but-slow, labeled 'slow', not wrong.
        golden = FakeCode({"EX": "1\n", "BIG": "timeout", "SMALL": "9\n"})
        ref = FakeCode({"EX": "1\n", "BIG": "ignored", "SMALL": "9\n"})
        orig = bm._sample_random_input
        # Big args -> "BIG"; after one shrink -> "SMALL".
        bm._sample_random_input = lambda gen, args, val, **k: (
            "BIG" if args and args[0][1] > 5 else "SMALL"
        )
        try:
            label, _ = bm._label_golden(golden, ref, object(), [(1, 100)], object(),
                                        _checker(), "EX", 2)
        finally:
            bm._sample_random_input = orig
        self.assertEqual(label, 'slow')

    def test_mismatch_hiding_behind_tle_is_caught_after_shrink(self):
        # Times out at full size, but disagrees on the shrunk input -> wrong-answer.
        golden = FakeCode({"EX": "1\n", "BIG": "timeout", "SMALL": "7\n"})
        ref = FakeCode({"EX": "1\n", "BIG": "ignored", "SMALL": "8\n"})
        orig = bm._sample_random_input
        bm._sample_random_input = lambda gen, args, val, **k: (
            "BIG" if args and args[0][1] > 5 else "SMALL"
        )
        try:
            label, witness = bm._label_golden(golden, ref, object(), [(1, 100)], object(),
                                              _checker(), "EX", 2)
        finally:
            bm._sample_random_input = orig
        self.assertEqual(label, 'wrong-answer')


class PairConfusionTests(unittest.TestCase):
    def test_each_relation_is_an_observation(self):
        # One wrong golden, 3 relations: flag, flag, pass -> TP=2, FN=1.
        corpus = [_gp_golden('wrong-answer', samples_verdicts=['flag', 'flag', 'pass'])]
        conf = bm._golden_pair_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual((conf['tp'], conf['fn'], conf['fp'], conf['tn']), (2, 1, 0, 0))
        self.assertAlmostEqual(conf['recall'], 2 / 3)

    def test_correct_golden_flags_are_fp(self):
        corpus = [_gp_golden('correct', samples_verdicts=['flag', 'pass', 'pass'])]
        conf = bm._golden_pair_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual((conf['fp'], conf['tn']), (1, 2))
        self.assertAlmostEqual(conf['fp_rate'], 1 / 3)

    def test_unknown_and_na_excluded(self):
        corpus = [
            _gp_golden('unknown', samples_verdicts=['flag', 'flag']),  # excluded (unknown gt)
            _gp_golden('wrong-answer', samples_verdicts=['flag', 'na']),      # na verdict excluded
        ]
        conf = bm._golden_pair_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual((conf['tp'], conf['fn']), (1, 0))
        self.assertEqual(conf['judged'], 1)

    def test_variant_key_respected(self):
        corpus = [_gp_golden('wrong-answer', example_verdicts=['pass'], samples_verdicts=['flag'])]
        prob = [_problem_with_corpus(corpus)]
        self.assertEqual(bm._golden_pair_confusion(prob, 'meta_example_verdicts')['tp'], 0)
        self.assertEqual(bm._golden_pair_confusion(prob, 'meta_samples_verdicts')['tp'], 1)

    def test_only_gate_pass_scored(self):
        corpus = [{'gate': 'fail', 'ground_truth': 'wrong-answer', 'meta_samples_verdicts': ['flag']},
                  _gp_golden('wrong-answer', samples_verdicts=['flag'])]
        conf = bm._golden_pair_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual(conf['judged'], 1)


class UnionConfusionTests(unittest.TestCase):
    def test_wrong_caught_if_any_relation_flags(self):
        corpus = [_gp_golden('wrong-answer', samples_verdicts=['pass', 'pass', 'flag'])]
        conf = bm._golden_union_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual((conf['tp'], conf['fn']), (1, 0))

    def test_correct_fp_if_any_relation_flags(self):
        corpus = [_gp_golden('correct', samples_verdicts=['pass', 'flag'])]
        conf = bm._golden_union_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual((conf['fp'], conf['tn']), (1, 0))

    def test_correct_tn_when_no_relation_flags(self):
        corpus = [_gp_golden('correct', samples_verdicts=['pass', 'pass'])]
        conf = bm._golden_union_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual((conf['fp'], conf['tn']), (0, 1))


class GoldenPopulationTests(unittest.TestCase):
    def test_census_and_base_rate(self):
        corpus = [
            _gp_golden('wrong-answer'), _gp_golden('correct'), _gp_golden('correct'),
            _gp_golden('slow'), _gp_golden('slow'),
            _gp_golden('unknown'),
            {'gate': 'fail', 'gate_reason': 'x'},
            {'gate': 'gen-failed'},
        ]
        pop = bm._golden_population([_problem_with_corpus(corpus)])
        self.assertEqual(pop['generated'], 8)
        self.assertEqual(pop['gate_passed'], 6)
        self.assertEqual((pop['wrong'], pop['correct'], pop['slow'], pop['unknown']),
                         (1, 2, 2, 1))
        # base rate is over DECISIVE goldens only (wrong-answer + correct); slow excluded.
        self.assertAlmostEqual(pop['base_rate_wrong'], 1 / 3)

    def test_slow_excluded_from_confusion(self):
        corpus = [
            _gp_golden('slow', samples_verdicts=['flag', 'pass']),  # excluded entirely
            _gp_golden('correct', samples_verdicts=['pass', 'pass']),
        ]
        conf = bm._golden_pair_confusion([_problem_with_corpus(corpus)], 'meta_samples_verdicts')
        self.assertEqual(conf['judged'], 2)  # only the 2 correct observations
        self.assertEqual((conf['fp'], conf['tn']), (0, 2))


class ExperimentAAggregateTests(unittest.TestCase):
    def _problem(self, ac_verdicts, wa_verdicts):
        return {'status': 'ok', 'ac_verdicts': ac_verdicts, 'wa_verdicts': wa_verdicts}

    def test_per_relation_ac_fp_and_wa(self):
        results = [
            self._problem(['flag', 'pass', 'pass'],
                          {'WA1': ['flag', 'flag', 'pass'], 'WA2': ['pass', 'pass', 'pass']}),
            self._problem(['pass', 'flag'],
                          {'WA1': ['flag', 'flag']}),
            {'status': 'declined'},  # no ac_verdicts -> ignored
        ]
        a = bm._aggregate_experiment_a(results)
        self.assertEqual(a['problems'], 2)
        self.assertEqual(a['relations'], 5)         # 3 + 2
        self.assertEqual(a['ac_flag'], 2)           # 1 + 1
        self.assertAlmostEqual(a['ac_fp_rate'], 2 / 5)
        # WA pairs: WA1(3)+WA2(3)+WA1(2) = 8; flags: 2 + 0 + 2 = 4
        self.assertEqual((a['wa_pairs'], a['wa_pair_flag']), (8, 4))
        self.assertAlmostEqual(a['wa_pair_rate'], 4 / 8)
        # Union: 3 WA instances, caught (WA1a yes, WA2a no, WA1b yes) -> 2/3
        self.assertEqual((a['wa_union_caught'], a['wa_union_total']), (2, 3))


class CheckerSourceRoundTripTests(unittest.TestCase):
    def test_builtin_sentinel(self):
        self.assertIs(bm._build_checker_from_source(bm._CHECKER_BUILTIN_SENTINEL).checker_func,
                      check_match)

    def test_custom_source(self):
        chk = bm._build_checker_from_source("def check(i, a, b):\n    return 'AC' if a == b else 'no'\n")
        self.assertEqual(chk.check("i", "x", "x"), 'AC')
        self.assertEqual(chk.check("i", "x", "y"), 'no')

    def test_missing_check_raises(self):
        with self.assertRaises(ValueError):
            bm._build_checker_from_source("def nope():\n    pass\n")


class ScoreRelationOnGoldensTests(unittest.TestCase):
    def test_appends_one_verdict_per_call(self):
        # A relation whose transform/relate always says OK -> 'pass' verdict.
        ok_module = ("def transform(s):\n    return s\n"
                     "def relate(a, b, c, d):\n    return 'OK'\n")
        from utils.code import Code
        from scripts.metamorphic import Metamorphic
        meta = Metamorphic(Code(ok_module))
        # Golden whose code just echoes; example-only path uses example_in.
        corpus = [{'gate': 'pass', 'ground_truth': 'correct',
                   'code_text': "import sys\nprint(sys.stdin.read())\n",
                   'meta_example_verdicts': [], 'meta_samples_verdicts': []},
                  {'gate': 'fail'}]
        # generator disabled -> samples verdict is 'na'.
        bm._score_relation_on_goldens(corpus, meta, "stmt", "EX\n", "EX\n",
                                      None, None, None, samples=1)
        g = corpus[0]
        self.assertEqual(len(g['meta_example_verdicts']), 1)
        self.assertEqual(g['meta_example_verdicts'][0], 'pass')
        self.assertEqual(g['meta_samples_verdicts'], ['na'])
        # gate-fail golden untouched.
        self.assertNotIn('meta_example_verdicts', corpus[1])


class GenerateGoldensParallelTests(unittest.TestCase):
    def test_collects_all_indices_concurrently(self):
        seen = []
        orig = bm._generate_golden

        def fake(provider, api_key, model, statement, example_in, example_out, index, **kw):
            seen.append(index)
            # workers run with quiet=False so the pool's single _quiet() suppresses them.
            self.assertFalse(kw.get('quiet', True))
            return f"code-{index}"

        bm._generate_golden = fake
        try:
            out = bm._generate_goldens_parallel("P", "K", "M", "stmt", "in", "out",
                                                num_goldens=5, workers=4)
        finally:
            bm._generate_golden = orig
        self.assertEqual(out, {i: f"code-{i}" for i in range(5)})
        self.assertEqual(sorted(seen), [0, 1, 2, 3, 4])

    def test_zero_goldens_returns_empty(self):
        self.assertEqual(
            bm._generate_goldens_parallel("P", "K", "M", "s", "i", "o", num_goldens=0),
            {})

    def test_worker_exception_becomes_none(self):
        orig = bm._generate_golden

        def fake(provider, api_key, model, statement, example_in, example_out, index, **kw):
            if index == 1:
                raise RuntimeError("boom")
            return f"code-{index}"

        bm._generate_golden = fake
        try:
            out = bm._generate_goldens_parallel("P", "K", "M", "s", "i", "o",
                                                num_goldens=3, workers=3)
        finally:
            bm._generate_golden = orig
        self.assertEqual(out[0], "code-0")
        self.assertIsNone(out[1])
        self.assertEqual(out[2], "code-2")


class GenerateOneRelationTests(unittest.TestCase):
    def test_retries_until_success(self):
        calls = {'n': 0}
        orig = bm._generate_metamorphic_with_validator

        def fake(provider, api_key, model, validator, statement, ei, eo, quiet=True):
            calls['n'] += 1
            if calls['n'] < 3:
                return None, {'stage': 'declined'}
            return 'META', None

        bm._generate_metamorphic_with_validator = fake
        try:
            meta, failure = bm._generate_one_relation("P", "K", "M", object(), "s", "i", "o",
                                                      attempts=4)
        finally:
            bm._generate_metamorphic_with_validator = orig
        self.assertEqual(meta, 'META')
        self.assertEqual(calls['n'], 3)

    def test_gives_up_after_attempts(self):
        orig = bm._generate_metamorphic_with_validator
        bm._generate_metamorphic_with_validator = \
            lambda *a, **k: (None, {'stage': 'metamorphic', 'error': 'x'})
        try:
            meta, failure = bm._generate_one_relation("P", "K", "M", object(), "s", "i", "o",
                                                      attempts=2)
        finally:
            bm._generate_metamorphic_with_validator = orig
        self.assertIsNone(meta)
        self.assertEqual(failure['stage'], 'metamorphic')


class GenerateRelationsParallelTests(unittest.TestCase):
    def test_collects_all_rounds_concurrently(self):
        seen = []
        orig = bm._generate_one_relation

        def fake(provider, api_key, model, validator, statement, ei, eo, attempts, **kw):
            seen.append('x')
            self.assertFalse(kw.get('quiet', True))
            return (f'meta', None)

        bm._generate_one_relation = fake
        try:
            out = bm._generate_relations_parallel("P", "K", "M", object(), "s", "i", "o",
                                                  rounds=4, attempts=1, workers=4)
        finally:
            bm._generate_one_relation = orig
        self.assertEqual(set(out.keys()), {1, 2, 3, 4})
        self.assertEqual(len(seen), 4)

    def test_zero_rounds_returns_empty(self):
        self.assertEqual(
            bm._generate_relations_parallel("P", "K", "M", object(), "s", "i", "o",
                                            rounds=0, attempts=1),
            {})

    def test_worker_exception_becomes_failure_tuple(self):
        orig = bm._generate_one_relation

        def fake(provider, api_key, model, validator, statement, ei, eo, attempts, **kw):
            raise RuntimeError("boom")

        bm._generate_one_relation = fake
        try:
            out = bm._generate_relations_parallel("P", "K", "M", object(), "s", "i", "o",
                                                  rounds=2, attempts=1, workers=2)
        finally:
            bm._generate_one_relation = orig
        for r in (1, 2):
            meta, failure = out[r]
            self.assertIsNone(meta)
            self.assertEqual(failure['stage'], 'metamorphic')


class FindProblemsRangeTests(unittest.TestCase):
    def _fake_tree(self, tmp, buckets):
        import os
        for b, probs in buckets.items():
            for p in probs:
                os.makedirs(os.path.join(tmp, b, p), exist_ok=True)

    def test_min_and_max_difficulty_filter(self):
        import os, tempfile
        tmp = tempfile.mkdtemp()
        self._fake_tree(tmp, {
            "difficulty_2000": ["a"], "difficulty_2100": ["b"],
            "difficulty_2200": ["c"], "difficulty_2300": ["d"], "difficulty_2400": ["e"],
        })
        orig = bm.DATA_DIR
        bm.DATA_DIR = tmp
        try:
            ge2200 = bm.find_problems(min_difficulty=2200)
            diffs = sorted({bm._extract_difficulty(p) for p in ge2200})
            self.assertEqual(diffs, [2200, 2300, 2400])

            band = bm.find_problems(min_difficulty=2100, max_difficulty=2300)
            self.assertEqual(sorted({bm._extract_difficulty(p) for p in band}),
                             [2100, 2200, 2300])
        finally:
            bm.DATA_DIR = orig


class ExecTimeoutTests(unittest.TestCase):
    def test_no_deadline_returns_cap(self):
        self.assertEqual(bm._exec_timeout(None), bm.EXEC_TIMEOUT_SEC)

    def test_caps_to_remaining_when_tight(self):
        to = bm._exec_timeout(time.time() + 3, cap=15)
        self.assertGreater(to, 0)
        self.assertLessEqual(to, 3.001)

    def test_uses_cap_when_plenty(self):
        self.assertEqual(bm._exec_timeout(time.time() + 1000, cap=15), 15)

    def test_past_deadline_small_positive(self):
        to = bm._exec_timeout(time.time() - 5, cap=15)
        self.assertGreater(to, 0)
        self.assertLessEqual(to, 1)


class RunProblemIsolatedTests(unittest.TestCase):
    def test_falls_back_in_process_when_no_budget(self):
        calls = {}
        orig = bm.run_problem

        def fake_run_problem(folder, provider, api_key, model, rounds, **kwargs):
            calls['args'] = (folder, provider, api_key, model, rounds)
            calls['kwargs'] = kwargs
            return {'problem': folder, 'status': 'ok'}

        bm.run_problem = fake_run_problem
        try:
            r = bm.run_problem_isolated('F', 'P', 'K', 'M', 5,
                                        hard_grace=30, problem_timeout=0, num_goldens=2)
        finally:
            bm.run_problem = orig
        self.assertEqual(r['status'], 'ok')
        self.assertEqual(calls['args'], ('F', 'P', 'K', 'M', 5))
        self.assertEqual(calls['kwargs'].get('num_goldens'), 2)
        self.assertNotIn('hard_grace', calls['kwargs'])


class UsageTrackingTests(unittest.TestCase):
    def setUp(self):
        from utils import usage
        usage.reset()

    def test_record_accumulates_and_snapshot(self):
        from utils import usage
        usage.record(prompt_tokens=10, completion_tokens=5, total_tokens=15, cost=0.001)
        usage.record(prompt_tokens=20, completion_tokens=4, total_tokens=24, cost=0.002)
        snap = usage.snapshot()
        self.assertEqual(snap['calls'], 2)
        self.assertEqual(snap['prompt_tokens'], 30)
        self.assertEqual(snap['completion_tokens'], 9)
        self.assertEqual(snap['total_tokens'], 39)
        self.assertAlmostEqual(snap['cost'], 0.003)

    def test_reset_clears(self):
        from utils import usage
        usage.record(total_tokens=5)
        usage.reset()
        self.assertEqual(usage.snapshot(),
                         {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0,
                          'total_tokens': 0, 'cost': 0.0})

    def test_record_tolerates_none(self):
        from utils import usage
        usage.record(prompt_tokens=None, completion_tokens=None,
                     total_tokens=None, cost=None)
        self.assertEqual(usage.snapshot()['calls'], 1)
        self.assertEqual(usage.snapshot()['total_tokens'], 0)

    def test_no_budget_means_never_over(self):
        from utils import usage
        usage.set_budget(None)
        usage.record(cost=100.0)
        self.assertFalse(usage.over_budget())

    def test_over_budget_when_cost_reaches_cap(self):
        from utils import usage
        usage.set_budget(1.0)
        usage.record(cost=0.4)
        self.assertFalse(usage.over_budget())
        usage.record(cost=0.7)  # cumulative 1.1 >= 1.0
        self.assertTrue(usage.over_budget())

    def test_reset_keeps_budget(self):
        from utils import usage
        usage.set_budget(1.0)
        usage.record(cost=2.0)
        self.assertTrue(usage.over_budget())
        usage.reset()
        # totals cleared, but the budget persists across problems in one process.
        self.assertFalse(usage.over_budget())
        usage.record(cost=1.5)
        self.assertTrue(usage.over_budget())

    def tearDown(self):
        from utils import usage
        usage.set_budget(None)
        usage.reset()


class UsageAggregateTests(unittest.TestCase):
    def test_sum_across_problems(self):
        results = [
            {'api_usage': {'calls': 2, 'prompt_tokens': 10, 'completion_tokens': 3,
                           'total_tokens': 13, 'cost': 0.01}},
            {'api_usage': {'calls': 1, 'prompt_tokens': 5, 'completion_tokens': 2,
                           'total_tokens': 7, 'cost': 0.02}},
            {'status': 'parse-error'},  # no api_usage -> skipped
        ]
        agg = bm._aggregate_usage(results)
        self.assertEqual(agg['problems'], 2)
        self.assertEqual(agg['calls'], 3)
        self.assertEqual(agg['total_tokens'], 20)
        self.assertAlmostEqual(agg['cost'], 0.03)

    def test_fmt_usage(self):
        s = bm._fmt_usage({'calls': 3, 'prompt_tokens': 100, 'completion_tokens': 20,
                           'total_tokens': 120, 'cost': 0.0123})
        self.assertIn("3 calls", s)
        self.assertIn("100+20=120 tokens", s)
        self.assertIn("$0.0123", s)
        self.assertEqual(bm._fmt_usage({}), "0 calls")


class OpenRouterUsageFieldTests(unittest.TestCase):
    def test_extracts_from_attribute(self):
        import utils.openrouter as orr

        class U:
            prompt_tokens = 11
            cost = 0.005
        self.assertEqual(orr._usage_field(U(), 'prompt_tokens'), 11)
        self.assertEqual(orr._usage_field(U(), 'cost'), 0.005)

    def test_extracts_from_model_extra(self):
        import utils.openrouter as orr

        class U:
            prompt_tokens = 11
            model_extra = {'cost': 0.009}
            cost = None
        self.assertEqual(orr._usage_field(U(), 'cost'), 0.009)

    def test_default_when_missing(self):
        import utils.openrouter as orr
        self.assertEqual(orr._usage_field(None, 'cost', 0.0), 0.0)

        class U:
            pass
        self.assertEqual(orr._usage_field(U(), 'total_tokens', 0), 0)


class OpenRouterBudgetGateTests(unittest.TestCase):
    def tearDown(self):
        from utils import usage
        usage.set_budget(None)
        usage.reset()

    def test_instruct_refuses_when_over_budget(self):
        from utils import usage
        import utils.openrouter as orr
        # Build an agent without touching the network (no API call should happen).
        agent = orr.OpenRouter_Agent.__new__(orr.OpenRouter_Agent)
        usage.set_budget(1.0)
        usage.record(cost=2.0)  # already over
        with self.assertRaises(RuntimeError) as cm:
            agent.instruct("hello")
        self.assertIn("cost cap", str(cm.exception).lower())


class ClaudePricingTests(unittest.TestCase):
    def test_known_models_by_substring(self):
        import utils.claude as c
        # opus calibrated to observed billing: $5 in + $25 out per MTok.
        self.assertAlmostEqual(c._estimate_cost('claude-opus-4-7', 1_000_000, 1_000_000), 30.0)
        self.assertAlmostEqual(c._estimate_cost('claude-sonnet-4-6', 1_000_000, 1_000_000), 18.0)
        self.assertAlmostEqual(c._estimate_cost('claude-haiku-4-5-20251001', 1_000_000, 1_000_000), 6.0)

    def test_opus_calibration_reproduces_real_bill(self):
        import utils.claude as c
        # 2026-06 Anthropic console: $13.09 for 255,262 in + 472,576 out on opus-4-7.
        self.assertAlmostEqual(c._estimate_cost('claude-opus-4-7', 255_262, 472_576), 13.09, places=1)

    def test_unknown_model_is_zero(self):
        import utils.claude as c
        self.assertEqual(c._estimate_cost('some-other-model', 1000, 1000), 0.0)
        self.assertEqual(c._estimate_cost(None, 1000, 1000), 0.0)

    def test_scales_with_tokens(self):
        import utils.claude as c
        # 2000 input + 500 output on sonnet ($3/$15 per MTok)
        expected = 2000 / 1e6 * 3.0 + 500 / 1e6 * 15.0
        self.assertAlmostEqual(c._estimate_cost('claude-sonnet-4-6', 2000, 500), expected)


class ClaudeBudgetGateTests(unittest.TestCase):
    def tearDown(self):
        from utils import usage
        usage.set_budget(None)
        usage.set_call_cap(None)
        usage.reset()

    def test_instruct_refuses_when_over_budget(self):
        from utils import usage
        import utils.claude as claude
        agent = claude.Claude_Agent.__new__(claude.Claude_Agent)
        usage.set_budget(1.0)
        usage.record(cost=2.0)
        with self.assertRaises(RuntimeError) as cm:
            agent.instruct("hi")
        self.assertIn("cost cap", str(cm.exception).lower())


class PerCallCapTests(unittest.TestCase):
    def tearDown(self):
        from utils import usage
        usage.set_budget(None)
        usage.set_call_cap(None)
        usage.reset()

    def _agent(self, messages, max_tokens=8192):
        import utils.claude as claude
        a = claude.Claude_Agent.__new__(claude.Claude_Agent)
        a.model_type = "claude-opus-4-7"
        a.max_tokens = max_tokens
        a.messages = messages
        return a

    def test_projected_cost_estimate(self):
        import utils.claude as c
        # 120k chars (~30k input tokens) at $5/MTok + 8192 out at $25/MTok.
        cost = c._projected_call_cost("claude-opus-4-7",
                                      [{"role": "user", "content": "x" * 120000}], "p", 8192)
        self.assertAlmostEqual(cost, 30000 / 1e6 * 5 + 8192 / 1e6 * 25, places=3)

    def test_refuses_runaway_call(self):
        from utils import usage
        usage.set_call_cap(1.0)
        # ~1M input tokens -> projected ~$5 > $1 cap -> refused before any network call.
        agent = self._agent([{"role": "user", "content": "x" * 4_000_000}])
        with self.assertRaises(RuntimeError) as cm:
            agent.instruct("go")
        self.assertIn("per-call cap", str(cm.exception).lower())

    def test_allows_normal_call_through_the_gate(self):
        # A normal-size call passes the per-call check (it then fails later trying to
        # reach the network, which proves the cap did NOT block it).
        from utils import usage
        usage.set_call_cap(1.0)
        agent = self._agent([{"role": "user", "content": "x" * 1000}])
        with self.assertRaises(Exception) as cm:
            agent.instruct("go")
        self.assertNotIn("per-call cap", str(cm.exception).lower())

    def test_no_cap_means_no_preflight_block(self):
        from utils import usage
        usage.set_call_cap(None)
        agent = self._agent([{"role": "user", "content": "x" * 4_000_000}])
        with self.assertRaises(Exception) as cm:
            agent.instruct("go")
        self.assertNotIn("per-call cap", str(cm.exception).lower())


class MarkdownGoldenSectionTests(unittest.TestCase):
    def test_empty_when_no_goldens(self):
        self.assertEqual(bm._format_golden_section([{'status': 'ok'}]), [])

    def test_renders_per_relation_and_population(self):
        corpus = [
            _gp_golden('wrong-answer', example_verdicts=['pass', 'pass'], samples_verdicts=['flag', 'flag']),
            _gp_golden('correct', example_verdicts=['pass', 'pass'], samples_verdicts=['pass', 'flag']),
        ]
        results = [_problem_with_corpus(corpus)]
        md = "\n".join(bm._format_golden_section(results))
        self.assertIn("Golden-solution evaluation", md)
        self.assertIn("No AC-based filtering", md)
        self.assertIn("Base rate wrong", md)
        self.assertIn("2000", md)  # per-difficulty row
        # strong-variant per-relation: wrong x2 flags=2 (recall 100%), correct x2 flags=1 (fp 50%)
        self.assertIn("Recall on wrong", md)


if __name__ == '__main__':
    unittest.main()
