from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "deepseek-ai/deepseek-coder-6.7b-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="cuda",  # or "cpu" if no GPU
    # trust_remote_code=True
)
with open("statement.txt", "r") as file:
    problem_statement = file.read()
prompt = f"Give me a python code that generates valid random test inputs for this problem: {problem_statement}\n I need the input generator code only."
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))