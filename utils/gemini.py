import utils.code as code
class Gemini_Agent:
    def __init__(self, API_KEY: str, model_type : str ='default'):
        import google.generativeai as genai
        import yaml
        genai.configure(api_key=API_KEY)
        if model_type == '2.5-pro':
            self.model = genai.GenerativeModel("gemini-2.5-pro")
        elif model_type == 'default' or model_type == '2.5-flash':
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.chat = self.model.start_chat()
    def instruct(self, prompt, code_only = False):
        text = self.chat.send_message(prompt).text
        if code_only:
            return code.Code(text)
        else:
            return text
