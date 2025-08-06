import os, time
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
    entry.config(foreground="gray")

def reset_text(text, placeholder):
    text.delete("1.0", "end")
    text.insert("1.0", placeholder)
    text.config(foreground="gray")


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
        entry.config(foreground="gray")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(foreground="white")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(foreground="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def set_text_placeholder(text, placeholder, value = None):
    if value:
        text.insert("1.0", value)
        text.config(foreground="white")
    else:
        text.insert("1.0", placeholder)
        text.config(foreground="gray")

    def on_focus_in(event):
        if text.get("1.0", "end-1c") == placeholder:
            text.delete("1.0", "end")
            text.config(foreground="white")

    def on_focus_out(event):
        if text.get("1.0", "end-1c").strip() == "":
            text.insert("1.0", placeholder)
            text.config(foreground="gray")

    text.bind("<FocusIn>", on_focus_in)
    text.bind("<FocusOut>", on_focus_out)

# ----- Submit callback -----
def check_signal(sq: Signal_Queue):
    while True:
        response = sq.check()
        if response != None:
            #messagebox.showinfo("Info", response.msg)
            print(response.field, response.msg)

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


# ----- Build UI -----
if __name__ == '__main__':
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)

    load_api_info()

    root = tb.Window(themename='darkly')
    root.title("CounterGen")
    root.geometry("700x950")

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
    main_input_frame = tb.Frame(root)
    main_input_frame.pack(pady=20, padx=15, fill="x")

    # Input 2 (left side)
    left_frame = tb.Frame(main_input_frame)
    left_frame.pack(side="left", padx=(0, 10))

    label2 = tb.Label(left_frame, text="Problem Info:", bootstyle="secondary")
    label2.pack(anchor="w")
    text2 = tb.Text(left_frame, height=15, width=40, wrap="word")
    text2.pack()
    set_text_placeholder(text2, "Paste problem description or link", load_file_content(f"{CACHE_PATH}/statement.txt"))

    # Input 3 and 4 (right stack)
    right_frame = tb.Frame(main_input_frame)
    right_frame.pack(side="left")

    label3 = tb.Label(right_frame, text="Example Input:", bootstyle="secondary")
    label3.pack(anchor="w")
    text3 = tb.Text(right_frame, height=6, width=30, wrap="word")
    text3.pack(pady=(0, 19))
    set_text_placeholder(text3, "Paste Example Input", load_file_content(f"{CACHE_PATH}/example_input.txt"))

    label4 = tb.Label(right_frame, text="Example Output:", bootstyle="secondary")
    label4.pack(anchor="w")
    text4 = tb.Text(right_frame, height=6, width=30, wrap="word")
    text4.pack()
    set_text_placeholder(text4, "Paste Example Output", load_file_content(f"{CACHE_PATH}/example_output.txt"))

    # Input 5 
    label5 = tb.Label(root, text="Incorrect Code:", bootstyle="secondary")
    label5.pack(anchor="w", padx=10, pady=(0, 0))
    text5 = tb.Text(root, height=4, width=70, wrap="word")
    text5.pack(padx=15)
    set_text_placeholder(text5, "Paste Failed Code", load_file_content(f"{CACHE_PATH}/WA.txt"))

    # Input 6 
    label6 = tb.Label(root, text="Correct Code:", bootstyle="secondary")
    label6.pack(anchor="w", padx=10, pady=(0, 0))
    text6 = tb.Text(root, height=4, width=70, wrap="word")
    text6.pack(padx=15)
    set_text_placeholder(text6, "Paste Correct Code (Optional)", load_file_content(f"{CACHE_PATH}/AC.txt"))

    progress_frame = tb.Frame(root)
    progress_frame.pack(pady=10)

    progress_label = tb.Label(progress_frame, text="Progress:", bootstyle="secondary")
    progress_label.pack(anchor="w")

    progressbar = tb.Progressbar(progress_frame, length=500, maximum=5)
    progressbar.pack()

    subtask_names = ["API", "Validator", "Generator", "AC Code", "Stress Test"]
    subtask_labels = []

    for name in subtask_names:
        lbl = tb.Label(progress_frame, text=f"🔄 {name}", bootstyle="info")
        lbl.pack(anchor="w", padx=20)
        subtask_labels.append(lbl)


    # Submit button
    button_frame = tb.Frame(root)
    button_frame.pack(pady=30)

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
