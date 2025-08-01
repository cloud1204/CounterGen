import subprocess, os
class Code:
    def __init__(self, text):
        if self.is_valid_python_code(text):
            self.code = text
        else:
            splited = text.split("```")
            self.code = splited[1]
            if self.code[:7] == 'python\n':
                self.code = self.code[7:]
            print(self.code)
    def is_valid_python_code(self, code: str) -> bool:
        try:
            compile(code, "<string>", "exec")
            return True
        except SyntaxError:
            return False
    def execute(self, input = "", args = [], timeout = -1):
        #
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