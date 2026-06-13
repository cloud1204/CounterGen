# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\nimport string\n\ndef generate_testcase(arg0, arg1, arg2, arg3):\n    t = random.randint(1, arg0)\n    print(t)\n    total_n = 0\n    max_total = arg1\n    for _ in range(t):\n        remaining = max_total - total_n\n        if remaining <= 1:\n            n = 1\n        else:\n            n = random.randint(1, min(arg1, remaining))\n        total_n += n\n        q = random.randint(1, arg2)\n        print(n, q)\n        alphabet_size = max(1, min(26, arg3))\n        chars = string.ascii_lowercase[:alphabet_size]\n        s = ''.join(random.choice(chars) for _ in range(n))\n        print(s)\n        for _ in range(q):\n            l = random.randint(1, n)\n            r = random.randint(l, n)\n            print(l, r)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    arg3 = int(sys.argv[4])\n    generate_testcase(arg0, arg1, arg2, arg3)\n", "<user>", "exec")

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
