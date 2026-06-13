# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(arg0, arg1, arg2):\n    t = random.randint(1, arg0)\n    cases = []\n    budget = 2**18\n    total = 0\n    for _ in range(t):\n        remaining_budget = budget - total\n        if remaining_budget < 2:\n            break\n        max_n = min(arg1, remaining_budget.bit_length() - 1)\n        if max_n < 1:\n            break\n        n = random.randint(1, max_n)\n        while (2**n) > remaining_budget:\n            n -= 1\n            if n < 1:\n                break\n        if n < 1:\n            break\n        total += 2**n\n        k = random.randint(1, n)\n        a = [random.randint(1, arg2) for _ in range(n)]\n        cases.append((n, k, a))\n\n    print(len(cases))\n    for n, k, a in cases:\n        print(n, k)\n        print(*a)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n", "<user>", "exec")

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
