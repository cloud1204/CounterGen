class Code:
    def __init__(self, text):
        splited = text.split("```")
        self.code = splited[1]
        if self.code[:7] == 'python\n':
            self.code = self.code[7:]
        print(self.code)
    def execute(self, input = ""):
        import subprocess, os
        filename = "temp_script.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.code)
        result = subprocess.run(["python", filename], input=input ,capture_output=True, text=True)
        os.remove("temp_script.py")
        return result