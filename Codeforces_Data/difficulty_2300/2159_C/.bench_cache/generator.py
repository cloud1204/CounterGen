# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(max_t, max_sum_n, max_val):\n    t = random.randint(1, max_t)\n    print(t)\n    remaining = max_sum_n\n    for i in range(t):\n        if i == t - 1:\n            n = random.randint(1, max(1, remaining))\n        else:\n            max_n = max(1, remaining - (t - i - 1))\n            n = random.randint(1, min(max_n, max(1, max_sum_n // max_t)))\n        remaining -= n\n        print(n)\n        \n        a = []\n        for j in range(n + 1):\n            if j == 0 or j == n:\n                a.append(-1)\n            else:\n                if random.random() < 0.5:\n                    a.append(-1)\n                else:\n                    a.append(random.randint(0, max_val))\n        print(' '.join(map(str, a)))\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n", "<user>", "exec")

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
