# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(arg0, arg1, arg2):\n    max_t = max(1, min(arg0, 10000))\n    t = random.randint(1, max_t)\n    \n    n_min = 3\n    m_min = 3\n    max_total_n = max(arg1, n_min)\n    max_total_m = max(arg2, m_min)\n    \n    cases = []\n    sum_n = 0\n    sum_m = 0\n    \n    for _ in range(t):\n        if sum_n + n_min > max_total_n or sum_m + m_min > max_total_m:\n            break\n        remaining_n = max_total_n - sum_n\n        remaining_m = max_total_m - sum_m\n        n_upper = max(n_min, min(remaining_n, max_total_n))\n        m_upper = max(m_min, min(remaining_m, max_total_m))\n        n = random.randint(n_min, n_upper)\n        m = random.randint(m_min, m_upper)\n        cases.append((n, m))\n        sum_n += n\n        sum_m += m\n    \n    if not cases:\n        cases.append((n_min, m_min))\n    \n    print(len(cases))\n    for n, m in cases:\n        print(n, m)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n", "<user>", "exec")

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
