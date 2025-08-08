import os, time, sys
import ttkbootstrap as tb
import threading
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

from utils.parse_statement import parse_statement
from scripts.CounterGen import CounterGen
from utils.signal import Signal_Queue
CACHE_PATH = "./Input_Cache"
API_DICT = {}
sq = Signal_Queue()

def reset_entry(entry, placeholder):
    entry.delete(0, "end")
    entry.insert(0, placeholder)
    entry.config(foreground="#4f4d4d")

def reset_text(text, placeholder):
    text.delete("1.0", "end")
    text.insert("1.0", placeholder)
    text.config(foreground="#4f4d4d")


def clear_all_inputs():
    #reset_entry(entry, "Enter API Key")
    reset_text(text2, "Paste problem description or link")
    reset_text(text3, "Paste Example Input")
    reset_text(text4, "Paste Example Output")
    reset_text(text5, "Paste Failed Code")
    reset_text(text6, "Paste Correct Code (Optional)")

def load_api_info():
    try:
        import yaml
        with open(f"{CACHE_PATH}/api_keys.yaml", "r") as stream:
            config = yaml.load(stream, Loader=yaml.SafeLoader)
            API_DICT['Gemini'] = config['Gemini']
            API_DICT['Claude'] = config['Claude']
            API_DICT['ChatGPT'] = config['ChatGPT']
            API_DICT['Last_Use'] = config['Last_Use']
    except FileNotFoundError:
        API_DICT['Gemini'] = None
        API_DICT['Claude'] = None
        API_DICT['ChatGPT'] = None
        API_DICT['Last_Use'] = None
        return

def load_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            return text if text != '' else None
    except FileNotFoundError:
        return None
    
def store_cache(API_Option, API_Key, Statement, Input, Output, WA, AC):
    API_DICT['Last_Use'] = API_Option
    API_DICT[API_Option] = API_Key
    with open(f"{CACHE_PATH}/api_keys.yaml", "w", encoding="utf-8") as f:
        content = f"Gemini: {API_DICT['Gemini']}\nClaude: {API_DICT['Claude']}\n" + \
        f"ChatGPT: {API_DICT['ChatGPT']}\nLast_Use: {API_DICT['Last_Use']}\n"
        f.write(content)
    with open(f"{CACHE_PATH}/statement.txt", "w", encoding="utf-8") as f:
        f.write(Statement) 
    with open(f"{CACHE_PATH}/example_input.txt", "w", encoding="utf-8") as f:
        f.write(Input)
    with open(f"{CACHE_PATH}/example_output.txt", "w", encoding="utf-8") as f:
        f.write(Output)     
    with open(f"{CACHE_PATH}/WA.txt", "w", encoding="utf-8") as f:
        f.write(WA)
    with open(f"{CACHE_PATH}/AC.txt", "w", encoding="utf-8") as f:
        f.write(AC)      


def set_entry_placeholder(entry, placeholder, value = None):
    if value:
        entry.insert(0, value)
        entry.config(foreground="white")
    else:
        entry.insert(0, placeholder)
        entry.config(foreground="#4f4d4d")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(foreground="white")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(foreground="#4f4d4d")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def set_text_placeholder(text, placeholder, value = None):
    if value:
        text.insert("1.0", value)
        text.config(foreground="white")
    else:
        text.insert("1.0", placeholder)
        text.config(foreground="#4f4d4d")

    def on_focus_in(event):
        if text.get("1.0", "end-1c") == placeholder:
            text.delete("1.0", "end")
            text.config(foreground="white")

    def on_focus_out(event):
        if text.get("1.0", "end-1c").strip() == "":
            text.insert("1.0", placeholder)
            text.config(foreground="#4f4d4d")

    text.bind("<FocusIn>", on_focus_in)
    text.bind("<FocusOut>", on_focus_out)

# ----- Submit callback -----
def check_signal(sq: Signal_Queue):
    while True:
        response = sq.check()
        if response != None:
            #messagebox.showinfo("Info", response.msg)
            print(response.field, response.msg)
            if response.field == "Stress Test" and response.type == 'succ':
                text_box_1.config(state="normal")  # enable writing
                text_box_1.insert("1.0", response.msg)
                text_box_1.config(state="disabled")
            if response.field == "Stress Test_cont" and response.type == 'succ':
                text_box_2.config(state="normal")  # enable writing
                text_box_2.insert("1.0", response.msg)
                text_box_2.config(state="disabled")

            if response.field in subtask_names:
                index = subtask_names.index(response.field)
                subtask_labels[index].config(text=f"✅ {response.field}", bootstyle="success")
                progressbar['value'] += 1
        time.sleep(1)
def on_submit():
    API_Option = type_var.get()
    API_Key = entry.get() if entry.get() != "Enter API Key" else ""

    inputs = [t.get("1.0", "end-1c") if t.get("1.0", "end-1c") not in placeholders else "" for t, placeholders in zip(texts, text_placeholders)]
    Statement = inputs[0]

    Statement = parse_statement(Statement)
    text2.delete("1.0", "end")
    set_text_placeholder(text2, "Paste problem description or link", Statement)

    Input = inputs[1]
    Output = inputs[2]
    WA = inputs[3]
    AC = inputs[4]

    store_cache(API_Option, API_Key, Statement, Input, Output, WA, AC)
    #CounterGen(API_Option, API_Key, Statement, Input, Output, WA, AC)
    threading.Thread(target=CounterGen, 
                     args=(sq, API_Option, API_Key, Statement, Input, Output, WA, AC), daemon=True).start()
    threading.Thread(target=check_signal, args=(sq,), daemon=True).start()

def create_text_frame(parent_frame, height, width, description, filename):
    text_frame = tb.Frame(parent_frame)
    text_frame.pack(fill="both", expand=True)
    text_scrollbar = tb.Scrollbar(text_frame, orient="vertical")
    text_scrollbar.pack(side="right", fill="y")
    text = tb.Text(text_frame, height=height, width=width, wrap="word", yscrollcommand=text_scrollbar.set)
    text.pack(fill="both", expand=True)
    text_scrollbar.config(command=text.yview)
    set_text_placeholder(text, description, load_file_content(f"{CACHE_PATH}/{filename}"))
    return text

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, msg):
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", msg)
        self.text_widget.see("end")  # auto-scroll
        self.text_widget.config(state="disabled")

    def flush(self):
        pass  # Needed for compatibility with sys.stdout

if __name__ == '__main__':
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)

    load_api_info()

    root = tb.Window(themename='darkly')
    root.title("CounterGen")
    root.geometry("1400x800")

    # Top: dropdown + single-line input
    frame1 = tb.Frame(root)
    frame1.pack(pady=(15, 0), padx=15, anchor="w")

    type_var = tb.StringVar(value="Gemini" if API_DICT["Last_Use"] == None else API_DICT["Last_Use"])
    type_menu = tb.Combobox(frame1, textvariable=type_var, values=["Gemini", "Claude", "ChatGPT"], width=10, bootstyle="info")
    type_menu.pack(side="left", padx=(0, 10))

    entry = tb.Entry(frame1, width=50, bootstyle="primary")
    entry.pack(side="left")
    set_entry_placeholder(entry, "Enter API Key", value=None if API_DICT["Last_Use"] == None else API_DICT[API_DICT["Last_Use"]])

    # Main input block: Input 2, 3, 4

    container_frame = tb.Frame(root)
    container_frame.pack(padx=15, pady=0, fill="both", expand=True)

    left_stack_frame = tb.Frame(container_frame)
    left_stack_frame.pack(side="left", fill="both", expand=True)

    main_input_frame = tb.Frame(left_stack_frame)
    main_input_frame.pack(fill="both", expand=True)

    # Input 2 (left side)
    left_frame = tb.Frame(main_input_frame)
    left_frame.pack(side="left", padx=(0, 10), fill="both", expand=True)

    label2 = tb.Label(left_frame, text="Problem Info:", foreground="#878686")
    label2.pack(anchor="w")

    text2 = create_text_frame(left_frame, 8, 20, "Paste problem description or link", 'statement.txt')

    # Input 3 and 4 (right stack)
    right_frame = tb.Frame(main_input_frame)
    right_frame.pack(side="left", fill="both", expand=True)


    label3 = tb.Label(right_frame, text="Example Input:", foreground="#878686")
    label3.pack(anchor="w")
    text3 = create_text_frame(right_frame, 3, 30, "Paste Example Input", "example_input.txt")

    label4 = tb.Label(right_frame, text="Example Output:", foreground="#878686")
    label4.pack(anchor="w")
    text4 = create_text_frame(right_frame, 3, 30, "Paste Example Output", "example_output.txt")


    code_input_frame = tb.Frame(left_stack_frame)
    code_input_frame.pack(fill="x", expand=True)
    # Input 5 
    label5 = tb.Label(code_input_frame, text="Incorrect Code:", foreground="#878686")
    label5.pack(anchor="w", padx=10, pady=(0, 0))
    text5 = create_text_frame(code_input_frame, 4, 50, "Paste Failed Code", "WA.txt")

    # Input 6 
    label6 = tb.Label(code_input_frame, text="Correct Code:", foreground="#878686")
    label6.pack(anchor="w", padx=10, pady=(0, 0))
    text6 = create_text_frame(code_input_frame, 4, 50, "Paste Correct Code (Optional)", "AC.txt")

    # Log Frame
    right_output_frame = tb.Frame(container_frame)
    right_output_frame.pack(side="left", fill="both", expand=True)
    tb.Label(right_output_frame, text="Terminal Log", foreground="#878686").pack(pady=0)
    output_box = tb.Text(right_output_frame, height=7, width=30, wrap="word")
    output_box.pack(fill="both", expand=True, padx=10, pady=(0,20))
    output_box.insert("1.0", "The terminal logs will show here\n")
    output_box.config(state="disabled", background="#1e1e1e", foreground="#666563")
    sys.stdout = TextRedirector(output_box)
    sys.stderr = TextRedirector(output_box)

    #
    bottom_text_frame = tb.Frame(right_output_frame)
    bottom_text_frame.pack(fill="both", expand=False, padx=10, pady=(0, 5))

    # First box (left)
    text_box_1 = tb.Text(bottom_text_frame, height=17, width=30, wrap="word")
    text_box_1.config(state="disabled", background="#1e1e1e", foreground="white")
    text_box_1.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=(0, 10))

    # Second box (right)
    text_box_2 = tb.Text(bottom_text_frame, height=17, width=30, wrap="word")
    text_box_2.config(state="disabled", background="#1e1e1e", foreground="white")
    text_box_2.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=(0, 10))


    progress_frame = tb.Frame(code_input_frame)
    progress_frame.pack(pady=10)

    progress_label = tb.Label(progress_frame, text="Progress:", foreground="#878686")
    progress_label.pack(anchor="w")

    progressbar = tb.Progressbar(progress_frame, length=500, maximum=6, bootstyle='success')
    progressbar.pack()

    subtask_names = ["API", "Validator", "Generator", "Checker", "AC Code", "Stress Test"]
    subtask_labels = []

    for name in subtask_names:
        lbl = tb.Label(progress_frame, text=f"🔄 {name}", bootstyle="info")
        lbl.pack(anchor="w", padx=20)
        subtask_labels.append(lbl)


    # Submit button
    button_frame = tb.Frame(code_input_frame)
    button_frame.pack(pady=10)

    submit_btn = tb.Button(button_frame, text="Submit", command=on_submit, bootstyle="success")
    submit_btn.pack(side="left", padx=10)

    clear_btn = tb.Button(button_frame, text="Reset", command=clear_all_inputs, bootstyle="danger")
    clear_btn.pack(side="left", padx=10)

    # For use in submission logic
    texts = [text2, text3, text4, text5, text6]
    text_placeholders = [
        "Paste problem description or link",
        "Paste Example Input",
        "Paste Example Output",
        "Paste Failed Code",
        "Paste Correct Code (Optional)"
    ]

    root.mainloop()
