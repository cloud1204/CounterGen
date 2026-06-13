# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\nfrom collections import Counter\n\ndef generate_testcase(arg0, arg1, arg2, arg3):\n    n = random.randint(1, arg0)\n    m = random.randint(1, arg1)\n    c = [random.randint(0, arg2) for _ in range(n)]\n    print(n, m)\n    print(*c)\n\n    herd = Counter(c)\n\n    for _ in range(m):\n        available_types = [k for k, v in herd.items() if v > 0]\n        if not available_types:\n            q = random.choice([1, 3])\n        else:\n            q = random.randint(1, 3)\n\n        if q == 1:\n            x = random.randint(0, arg2)\n            herd[x] += 1\n            print(1, x)\n        elif q == 2:\n            x = random.choice(available_types)\n            herd[x] -= 1\n            print(2, x)\n        else:\n            x = random.randint(1, arg3)\n            print(3, x)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    arg3 = int(sys.argv[4])\n    generate_testcase(arg0, arg1, arg2, arg3)\n", "<user>", "exec")

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
