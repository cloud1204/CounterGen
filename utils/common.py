import subprocess, os, random, tempfile
class Code:
    def __init__(self, text):
        self.language = 'python'
        self.filename = ''
        if self.is_cpp_code(text):
            self.language = 'cpp'
            self.filename = 'tmp' + str(random.randint(10000, 99999))
            with open(f"tmp_storage/{self.filename}.cpp", "w", encoding="utf-8") as f:
                f.write(text)
            compile_cmd = ["g++", f"tmp_storage/{self.filename}.cpp", "-o", f"tmp_storage/{self.filename}"]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
            if compile_result.returncode != 0:
                print('Compile error')
                print(compile_result.stderr)
            else:
                print('Compile success')
        elif self.is_valid_python_code(text):
            self.code = text
        else:
            splited = text.split("```")
            self.code = splited[1]
            if self.code[:7] == 'python\n':
                self.code = self.code[7:]
            print(self.code)
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
