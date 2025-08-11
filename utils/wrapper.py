def cpp_wrap(org_code: str) -> str:
    new_code = f"#define main user_main\n{org_code}\n#undef main\n"
    new_code += "#include <bits/stdc++.h>\nusing namespace std;\n"
    new_code += '''
    int main() {
    ios::sync_with_stdio(false);
        cin.tie(nullptr);
        int T;
        if (!(cin >> T)) return 0;
        while (T--) {
            user_main(); // Call the renamed user's main
        }
    }
    '''
    return new_code
    
def python_wrap(org_code: str) -> str:
    # """
    # Wrap a Python program so it reads T, then executes the original code T times.
    # Each run keeps reading from the same stdin (no L1/L2 lengths).
    # Swallows user exits:
    #   - sys.exit(), exit(), quit()  -> caught as SystemExit
    #   - os._exit(...)               -> temporarily patched to raise SystemExit
    # """
    new_code = f'''# === AUTO-GENERATED WRAPPER ===
import sys, os, builtins

# Compile original code once
_CODE = compile({org_code!r}, "<user>", "exec")

def user_main():
    # Fresh globals for each run; user code sees __name__ == "__main__"
    ns = {{"__name__": "__main__", "__file__": "<user>", "__builtins__": builtins, "sys": sys, "os": os}}

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
        sys.stdout.flush()

if __name__ == "__main__":
    main()
'''
    return new_code