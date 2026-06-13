# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(arg0, arg1, arg2):\n    t = random.randint(1, arg0)\n    print(t)\n    max_total = arg1\n    remaining = max_total\n    cases = []\n    for i in range(t):\n        if i == t - 1:\n            n = random.randint(1, max(1, min(remaining, arg1)))\n        else:\n            n = random.randint(1, max(1, min(remaining - (t - i - 1), arg1)))\n        remaining -= n\n        cases.append(n)\n\n    for n in cases:\n        print(n)\n        print(*[random.randint(-arg2, arg2) for _ in range(n)])\n        a = list(range(1, n + 1))\n        random.shuffle(a)\n        print(*a)\n        b = list(range(1, n + 1))\n        random.shuffle(b)\n        print(*b)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n", "<user>", "exec")

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
