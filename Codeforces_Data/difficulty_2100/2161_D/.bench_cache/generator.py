# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(arg0, arg1, arg2):\n    MAX_SUM_N = arg1\n    MAX_T = min(arg0, MAX_SUM_N)\n    \n    t = random.randint(1, MAX_T)\n    print(t)\n    \n    remaining = MAX_SUM_N\n    for i in range(t):\n        if i == t - 1:\n            n = random.randint(1, remaining)\n        else:\n            max_n = remaining - (t - i - 1)\n            n = random.randint(1, max(1, min(max_n, arg1)))\n        remaining -= n\n        print(n)\n        print(' '.join(str(random.randint(1, min(n, arg2))) for _ in range(n)))\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n", "<user>", "exec")

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
