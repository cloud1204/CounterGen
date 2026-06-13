# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(arg0, arg1, arg2, arg3):\n    t = random.randint(1, arg0)\n    print(t)\n    remaining = arg1\n    cases = []\n    for i in range(t):\n        if i == t - 1:\n            max_cells = remaining\n        else:\n            max_cells = max(1, remaining - (t - i - 1))\n        \n        max_cells = min(max_cells, arg2)\n        \n        while True:\n            n = random.randint(1, min(max_cells, arg2))\n            m_max = min(max_cells // n, arg2)\n            if m_max >= 1:\n                m = random.randint(1, m_max)\n                break\n        \n        cases.append((n, m))\n        remaining -= n * m\n    \n    for n, m in cases:\n        print(n, m)\n        grid = [[random.randint(-arg3, arg3) for _ in range(m)] for _ in range(n)]\n        has_nonneg = any(grid[i][j] >= 0 for i in range(n) for j in range(m))\n        if not has_nonneg:\n            i = random.randint(0, n - 1)\n            j = random.randint(0, m - 1)\n            grid[i][j] = random.randint(0, arg3)\n        for row in grid:\n            print(*row)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    arg3 = int(sys.argv[4])\n    generate_testcase(arg0, arg1, arg2, arg3)\n", "<user>", "exec")

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
