# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(arg0, arg1, arg2, arg3):\n    MAX_SUM_N2 = arg1 * arg1\n    MAX_N = arg1\n    COEF_MIN = -arg2\n    COEF_MAX = arg2\n\n    t = random.randint(1, arg0)\n    test_cases = []\n    remaining = MAX_SUM_N2\n\n    for i in range(t):\n        if remaining <= 0:\n            break\n        max_n_here = min(MAX_N, int(remaining ** 0.5))\n        if max_n_here < 1:\n            break\n        if i == t - 1:\n            n = random.randint(1, max_n_here)\n        else:\n            n = random.randint(1, min(max_n_here, arg3))\n        remaining -= n * n\n        test_cases.append(n)\n\n    actual_t = len(test_cases)\n    print(actual_t)\n\n    for n in test_cases:\n        print(n)\n        seen = set()\n        count = 0\n        while count < n:\n            a = random.randint(COEF_MIN, COEF_MAX)\n            if a == 0:\n                continue\n            b = random.randint(COEF_MIN, COEF_MAX)\n            c = random.randint(COEF_MIN, COEF_MAX)\n            if (a, b, c) in seen:\n                continue\n            seen.add((a, b, c))\n            print(a, b, c)\n            count += 1\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    arg3 = int(sys.argv[4])\n    generate_testcase(arg0, arg1, arg2, arg3)\n", "<user>", "exec")

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
