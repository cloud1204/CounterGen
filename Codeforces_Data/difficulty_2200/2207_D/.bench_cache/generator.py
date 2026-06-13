# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile("import random, sys\n\ndef generate_testcase(max_t, max_sum_n, max_n_per_case):\n    t = random.randint(1, max_t)\n    print(t)\n    \n    remaining = max_sum_n\n    cases = []\n    for i in range(t):\n        if i == t - 1:\n            n = max(3, min(remaining, max_n_per_case))\n        else:\n            max_n = remaining - 3 * (t - i - 1)\n            max_n = min(max_n, max_n_per_case)\n            if max_n < 3:\n                max_n = 3\n            n = random.randint(3, max_n)\n        remaining -= n\n        if remaining < 0:\n            remaining = 0\n        cases.append(n)\n    \n    for n in cases:\n        edges = []\n        for i in range(2, n + 1):\n            p = random.randint(1, i - 1)\n            edges.append((p, i))\n        \n        degree = [0] * (n + 1)\n        for a, b in edges:\n            degree[a] += 1\n            degree[b] += 1\n        \n        non_leaves = [i for i in range(1, n + 1) if degree[i] > 1]\n        \n        if not non_leaves:\n            v = 1\n        else:\n            v = random.choice(non_leaves)\n        \n        k = random.randint(1, n)\n        print(n, k, v)\n        \n        random.shuffle(edges)\n        for a, b in edges:\n            if random.random() < 0.5:\n                a, b = b, a\n            print(a, b)\n\nif __name__ == '__main__':\n    arg0 = int(sys.argv[1])\n    arg1 = int(sys.argv[2])\n    arg2 = int(sys.argv[3])\n    generate_testcase(arg0, arg1, arg2)\n", "<user>", "exec")

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
