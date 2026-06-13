# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile('import random, sys\n\ndef generate_testcase(arg0, arg1, arg2, arg3):\n    out = sys.stdout.write\n    T = random.randint(1, arg0)\n    \n    max_total_n = arg1\n    max_total_m = arg2\n    \n    avg_n = max(1, max_total_n // T)\n    avg_m = max(0, max_total_m // T)\n    \n    remaining_n = max_total_n\n    remaining_m = max_total_m\n    \n    cases = []\n    for t in range(T):\n        rem_cases = T - t\n        max_n_here = remaining_n - (rem_cases - 1)\n        max_n_here = max(1, min(max_n_here, 2 * avg_n))\n        n = random.randint(1, max_n_here)\n        remaining_n -= n\n        \n        min_m = n - 1 if n > 1 else 0\n        max_m_here = remaining_m - (rem_cases - 1) * 0\n        max_m_here = max(min_m, min(max_m_here, 2 * avg_m + min_m))\n        \n        if min_m > remaining_m:\n            n = 1\n            min_m = 0\n            max_m_here = max(0, min(remaining_m, 2 * avg_m))\n        \n        m = random.randint(min_m, max_m_here)\n        remaining_m -= m\n        \n        cases.append((n, m))\n    \n    lines = []\n    lines.append(f"{T}\\n")\n    \n    for n, m in cases:\n        lines.append(f"{n} {m}\\n")\n        if n > 1:\n            nodes = list(range(1, n + 1))\n            random.shuffle(nodes)\n            tree_edges = []\n            for i in range(1, n):\n                u = nodes[i]\n                v = nodes[random.randint(0, i - 1)]\n                w = random.randint(1, arg3)\n                tree_edges.append((u, v, w))\n            extra = m - (n - 1)\n            extra_edges = []\n            for _ in range(extra):\n                u = random.randint(1, n)\n                v = random.randint(1, n)\n                w = random.randint(1, arg3)\n                extra_edges.append((u, v, w))\n            all_edges = tree_edges + extra_edges\n            random.shuffle(all_edges)\n        else:\n            all_edges = []\n            for _ in range(m):\n                w = random.randint(1, arg3)\n                all_edges.append((1, 1, w))\n        \n        for u, v, w in all_edges:\n            lines.append(f"{u} {v} {w}\\n")\n    \n    sys.stdout.write("".join(lines))\n\nif __name__ == \'__main__\':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    arg3 = int(sys.argv[4])\n    generate_testcase(arg0, arg1, arg2, arg3)\n', "<user>", "exec")

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
