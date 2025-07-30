import requests, random, subprocess

def Query_LLM(prompt, API_KEY):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    api_key = "AIzaSyA-ZbvxPhsPvMukYlddmYmXQehcMTJjwr4"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    return text

class Code:
    def __init__(self, text):
        splited = text.split("```")
        self.code = splited[1]
        if self.code[:7] == 'python\n':
            self.code = self.code[7:]
        print(self.code)
    def execute(self, input = ""):
        filename = "temp_script.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.code)
        result = subprocess.run(["python", filename], input=input ,capture_output=True, text=True)
        return result.stdout
    
if __name__ == "__main__":
    import yaml
    with open("api_keys.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.SafeLoader)
    API_KEY = config['gemini']
    print(API_KEY)
    with open("statement.txt", "r") as file:
        problem_statement = file.read()
        prompt = f"Give me a python code that generates valid random test inputs for this problem: {problem_statement}\nI need the input generator code only."
    text = Query_LLM(prompt, API_KEY)

    testcase = Code(text).execute()
    text = Query_LLM(f"Also give me a validator python code to make sure the input is valid and satisfy all constraint in this problem. The validator should simply output 'valid' when the input (from standard IO) is valid, otherwise output 'invalid' along with the reason. {problem_statement}\nI need the validator code only.", API_KEY)
    
    validator = Code(text)
    print(validator.execute(testcase))