# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(arg0, arg1, arg2):\n    t = random.randint(1, arg0)\n    print(t)\n    max_n_total = arg1\n    max_m_total = arg2\n    for _ in range(t):\n        n = random.randint(2, max(2, min(arg1, max_n_total)))\n        m = random.randint(1, max(1, min(arg2, max_m_total)))\n        max_n_total -= n\n        max_m_total -= m\n        if max_n_total < 2:\n            max_n_total = 2\n        if max_m_total < 1:\n            max_m_total = 1\n        print(n, m)\n        for _ in range(m):\n            l = random.randint(1, n - 1)\n            r = random.randint(l + 1, n)\n            print(l, r)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n", "<user>", "exec")

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
