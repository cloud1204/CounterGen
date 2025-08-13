import subprocess, random, re

def split_output(output: str, separate_pattern : str = "!@#s_p&^%") -> list[str]:
    return output.split(separate_pattern)[:-1]

class Code:
    def __init__(self, text):
        self.language = 'python'
        self.filename = ''
        if self.is_cpp_code(text):
            self.language = 'cpp'
            self.code = text
            self.compile_cpp()
        elif self.is_valid_python_code(text):
            self.code = text
            print(self.code)
        else: # Default: python code
            matches = re.findall(r"```(.*?)```", text, re.DOTALL)
            self.code = matches[0]
            if self.code[:7] == 'python\n':
                self.code = self.code[7:]
            print(self.code)
            assert self.is_valid_python_code(self.code)
    def compile_cpp(self):
        self.filename = 'tmp' + str(random.randint(10000, 99999))
        with open(f"tmp_storage/{self.filename}.cpp", "w", encoding="utf-8") as f:
            f.write(self.code)
        compile_cmd = ["g++", f"tmp_storage/{self.filename}.cpp", "-o", f"tmp_storage/{self.filename}"]
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
        if compile_result.returncode != 0:
            print('Compile error')
            print(compile_result.stderr)
            raise ValueError("Compile Error")
        else:
            print('Compile success')
    def is_cpp_code(self, code: str) -> bool:
        cpp_keywords = [
            "#include", "# include", "std::", "using namespace std", "int main(", "int main ("
        ]
        return any(kw in code for kw in cpp_keywords)
    def is_valid_python_code(self, code: str) -> bool:
        try:
            compile(code, "<string>", "exec")
            return True
        except SyntaxError:
            return False
    def execute(self, input = "", args = [], timeout = -1):
        if self.language == 'python':
            command = ["python", "-c", self.code] + [str(arg) for arg in args]
            if timeout == -1:
                result = subprocess.run(command, input=input, capture_output=True, text=True)
            else:
                try:
                    result = subprocess.run(
                        command, input=input, timeout=timeout, capture_output=True, text=True
                    )
                except subprocess.TimeoutExpired:
                    return 'timeout'
            return result
        elif self.language == 'cpp':
            try:
                result = subprocess.run(
                    [f"./tmp_storage/{self.filename}"] + [str(arg) for arg in args],
                    input=input,
                    timeout=None if timeout == -1 else timeout,
                    capture_output=True,
                    text=True,
                )
            except subprocess.TimeoutExpired:
                result = "timeout"
            return result
        else:
            raise ValueError("Code language not defined")
    def wrap(self):
        if self.language == 'cpp':
            self.cpp_wrap()
            self.compile_cpp()
        if self.language == 'python':
            self.python_wrap()
    
    def cpp_wrap(self, separate_pattern = "!@#s_p&^%"):
        new_code = f"#define main user_main\n{self.code}\n#undef main\n"
        new_code += "#include <bits/stdc++.h>\nusing namespace std;\n"
        new_code += f'''
        signed main() {{
            ios::sync_with_stdio(false);
            cin.tie(nullptr);
            int T;
            if (!(cin >> T)) return 0;
            while (T--) {{
                user_main();
                cout << "{separate_pattern}";
            }}
            return 0;
        }}
        '''
        self.code = new_code
        
    def python_wrap(self, separate_pattern = "!@#s_p&^%"):
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
_CODE = compile({self.code!r}, "<user>", "exec")

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
        sys.stdout.write("{separate_pattern}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
'''
        self.code = new_code
        assert self.is_valid_python_code(self.code)


