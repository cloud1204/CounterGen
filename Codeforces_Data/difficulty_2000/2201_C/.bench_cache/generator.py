# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile('import random, sys\n\ndef gen_regular(n):\n    if n == 0:\n        return ""\n    result = []\n    open_count = 0\n    close_count = 0\n    half = n // 2\n    for _ in range(n):\n        can_open = open_count < half\n        can_close = close_count < open_count\n        if can_open and can_close:\n            if random.random() < 0.5:\n                result.append(\'(\')\n                open_count += 1\n            else:\n                result.append(\')\')\n                close_count += 1\n        elif can_open:\n            result.append(\'(\')\n            open_count += 1\n        else:\n            result.append(\')\')\n            close_count += 1\n    return "".join(result)\n\ndef generate_testcase(arg0, arg1, arg2):\n    t = random.randint(1, arg0)\n    print(t)\n    remaining = arg2\n    for i in range(t):\n        left = t - i\n        max_n = remaining - 2 * (left - 1)\n        max_n = min(max_n, arg1)\n        if max_n < 2:\n            max_n = 2\n        n = random.randint(1, max_n // 2) * 2\n        remaining -= n\n        print(n)\n        print(gen_regular(n))\n\nif __name__ == \'__main__\':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n', "<user>", "exec")

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
