# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile('import random, sys\n\ndef gen_test_case(n_max):\n    n = random.randint(2, n_max)\n    max_m = n - 2\n    if max_m <= 0:\n        return n, []\n    \n    target_m = random.randint(0, max_m)\n    if target_m == 0:\n        return n, []\n    \n    intervals = [(1, n)]\n    chosen = []\n    \n    while len(chosen) < target_m and intervals:\n        idx = random.randrange(len(intervals))\n        intervals[idx], intervals[-1] = intervals[-1], intervals[idx]\n        lo, hi = intervals.pop()\n        if hi - lo < 2:\n            continue\n        \n        u = random.randint(lo, hi - 2)\n        v = random.randint(u + 2, hi)\n        \n        chosen.append((u, v))\n        \n        if u - lo >= 2:\n            intervals.append((lo, u))\n        if v - u >= 2:\n            intervals.append((u, v))\n        if hi - v >= 2:\n            intervals.append((v, hi))\n    \n    unique_set = set()\n    unique_chosen = []\n    for e in chosen:\n        if e not in unique_set:\n            unique_set.add(e)\n            unique_chosen.append(e)\n    \n    return n, unique_chosen\n\ndef generate_testcase(arg0, arg1, arg2):\n    total_n_budget = arg2\n    max_t = arg0\n    max_n = arg1\n    \n    test_cases = []\n    used = 0\n    \n    t_target = random.randint(1, max_t)\n    \n    for _ in range(t_target):\n        remaining = total_n_budget - used\n        if remaining < 2:\n            break\n        n_max = min(max_n, remaining)\n        if n_max < 2:\n            break\n        n, edges = gen_test_case(n_max)\n        used += n\n        test_cases.append((n, edges))\n    \n    if not test_cases:\n        n_max = min(max_n, max(2, total_n_budget))\n        n_max = max(n_max, 2)\n        n, edges = gen_test_case(n_max)\n        test_cases.append((n, edges))\n    \n    out = []\n    out.append(str(len(test_cases)))\n    for n, edges in test_cases:\n        out.append(f"{n} {len(edges)}")\n        for u, v in edges:\n            out.append(f"{u} {v}")\n    sys.stdout.write("\\n".join(out) + "\\n")\n\nif __name__ == \'__main__\':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n', "<user>", "exec")

def user_main():
    # Fresh globals for each run; user code sees __name__ == "__main__"
    ns = {"__name__": "__main__", "__file__": "<user>", "__builtins__": builtins, "sys": sys, "os": os}

    # Patch os._exit so it doesn't kill the whole process
    _orig_os_exit = getattr(os, "_exit", None)
    def _blocked_os_exit(status=0):
        raise SystemExit(status)
    if _orig_os_exit is not None:
        os._exit = _blocked_os_exit

    try:
        exec(_CODE, ns)
    except SystemExit:
        # Swallow user-requested exit for this test only
        pass
    finally:
        # Restore original os._exit
        if _orig_os_exit is not None:
            os._exit = _orig_os_exit

def main():
    line = sys.stdin.readline()
    try:
        T = int(line.strip())
    except Exception:
        T = 0
    for _ in range(T):
        user_main()
        sys.stdout.write("!@#s_p&^%")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
