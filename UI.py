import os, time, sys
import yaml
import ttkbootstrap as tb
import threading
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

from utils.parse_statement import parse_statement
from scripts.CounterGen import CounterGen
from utils.signal import Signal_Queue
CACHE_PATH = "./Input_Cache"
SETTINGS = {}
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

def reset_outputs():
    progressbar['value'] = 0
    for name in subtask_names:
        index = subtask_names.index(name)
        subtask_labels[index].config(text=f"⏳ {name}", bootstyle="info")
    # reset terminal logs
    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", "The terminal logs will show here\n")
    output_box.config(state="disabled")
    # reset output logs
    text_box_1.config(state="normal") 
    text_box_1.delete("1.0", "end") 
    text_box_1.config(state="disabled")
    text_box_2.config(state="normal") 
    text_box_2.delete("1.0", "end") 
    text_box_2.config(state="disabled")

def reset():
    clear_all_inputs()
    reset_outputs()

def load_api_info():
    global SETTINGS
    if not os.path.exists(f"{CACHE_PATH}/settings.yaml"):
        import shutil
        shutil.copy(f"{CACHE_PATH}/settings_template.yaml", f"{CACHE_PATH}/settings.yaml")
    with open(f"{CACHE_PATH}/settings.yaml", "r") as stream:
        SETTINGS = yaml.load(stream, Loader=yaml.SafeLoader)

def load_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            return text if text != '' else None
    except FileNotFoundError:
        return None
    
def store_cache(API_Option, API_Key, Statement, Input, Output, WA, AC):
    SETTINGS['Last_Use'] = API_Option
    SETTINGS[API_Option]['API_KEY'] = API_Key

    with open(f"{CACHE_PATH}/settings.yaml", "w") as f:
        yaml.dump(SETTINGS, f, default_flow_style=False)
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
    entry.delete(0, "end")
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
            if response.type != 'start':
                if response.field == "Stress Test" and response.type == 'succ':
                    pass
                else:
                    print(response.msg)
            if response.field == "Stress Test" and response.type == 'succ':
                testcase, fail_reason = response.msg
                text_box_1.config(state="normal")  # enable writing
                text_box_1.insert("1.0", testcase)
                text_box_1.config(state="disabled")
                text_box_2.config(state="normal") 
                text_box_2.insert("1.0", fail_reason)
                text_box_2.config(state="disabled")

            if response.type == 'fail':
                sq.shutdown()
            
            if response.type == 'start' and response.field in subtask_names:
                index = subtask_names.index(response.field)
                subtask_labels[index].config(text=f"🔄 {response.field}", bootstyle="warning", font=("Segoe UI Emoji", 9))
            if response.type == 'succ' and response.field in subtask_names:
                index = subtask_names.index(response.field)
                subtask_labels[index].config(text=f"✅ {response.field}", bootstyle="success", font=("Segoe UI Emoji", 9))
                progressbar['value'] += 1
        if not sq.main_thread.is_alive():
            submit_btn.config(
                text="Submit", command=on_submit, bootstyle="success"
            )
            sq.reset()
        time.sleep(0.3)
def on_submit():
    reset_outputs()
    submit_btn.config(
        text=" Stop ",
        command=on_stop,
        bootstyle="danger"
    )

    API_Option = type_var.get()
    API_Key = entry.get() if entry.get() != "Enter API Key" else ""

    inputs = [t.get("1.0", "end-1c") if t.get("1.0", "end-1c") not in placeholders else "" for t, placeholders in zip(texts, text_placeholders)]
    Statement = inputs[0]

    Statement, _Input, _Output = parse_statement(Statement)
    Input = inputs[1] if _Input == None else _Input
    Output = inputs[2] if _Output == None else _Output

    text2.delete("1.0", "end")
    set_text_placeholder(text2, "Paste problem description or link", Statement)
    text3.delete("1.0", "end")
    set_text_placeholder(text3, "", Input)
    text4.delete("1.0", "end")
    set_text_placeholder(text4, "", Output)

    WA = inputs[3]
    AC = inputs[4]

    store_cache(API_Option, API_Key, Statement, Input, Output, WA, AC)
    sq.main_thread = threading.Thread(target=CounterGen, 
                     args=(sq, SETTINGS.copy(), Statement, Input, Output, WA, AC), daemon=True)
    sq.main_thread.start()
    threading.Thread(target=check_signal, args=(sq,), daemon=True).start()

def on_stop():
    sq.shutdown()
    time.sleep(5)

def open_settings():
    if hasattr(root, "settings_window") and root.settings_window.winfo_exists():
        root.settings_window.lift()
        return
    
    overlay = tk.Toplevel(root)
    overlay.overrideredirect(True)  # remove window decorations
    overlay.attributes("-alpha", 0.3)  # set transparency (0.0 to 1.0)
    overlay.configure(bg='black')
    overlay.geometry(f"{root.winfo_width()}x{root.winfo_height()}+{root.winfo_x()}+{root.winfo_y()}")
    overlay.lift()
    overlay.transient(root)

    settings = tb.Toplevel(root)
    settings.title("Advanced Settings")
    settings.grab_set()

    root.update_idletasks()
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    settings_x = root_x + root_width - 500  
    settings_y = root_y + 35                

    settings.geometry(f"500x350+{settings_x}+{settings_y}")

    settings.resizable(False, False)
    settings.attributes("-topmost", True)

    root.settings_window = settings

    model_name = SETTINGS['Last_Use']
    if model_name == 'Gemini':
        model_options = ['gemini-2.5-flash', 'gemini-2.5-pro']
    elif model_name == 'Claude':
        model_options = ['claude-3-7-sonnet-latest', 'claude-sonnet-4-0', 'claude-opus-4-0', 'claude-opus-4-1']
    elif model_name == 'OpenAI':
        model_options = ['C', 'D']
    else:
        model_options = []

    # Utility: create labeled combo rows
    def add_combobox_row(parent, label_text, values, default_value, readonly=True, index=''):
        row = tb.Frame(parent)
        row.pack(fill="x", padx=10, pady=5)

        label = tb.Label(row, text=label_text, width=30, anchor="w")
        label.pack(side="left")

        var = tb.StringVar()
        combo = tb.Combobox(row, textvariable=var, values=values, width=20)
        combo.pack(side="left", fill="x", expand=True)

        combo.bind("<<ComboboxSelected>>", lambda e, n=index: on_selected(e, n))

        if readonly:
            combo.config(state="readonly")

        settings.after(10, combo.set, default_value)
        return var

    # Section title
    tb.Label(settings, text="Model Options", font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))

    def on_selected(event, index):
        value = event.widget.get()
        if index == 'TL':
            SETTINGS['Time_Limit_Per_Batch'] = int(value)
        else:
            SETTINGS[model_name][index] = value

    val_gen_var = add_combobox_row(
        settings,
        "Validator/Generator Model:",
        model_options,
        SETTINGS[model_name]['val/gen'],
        index='val/gen'
    )

    checker_var = add_combobox_row(
        settings,
        "Output Checker Model:",
        model_options,
        SETTINGS[model_name]['checker'],
        index='checker'
    )

    ac_var = add_combobox_row(
        settings,
        "AC Code Model:",
        model_options,
        SETTINGS[model_name]['AC'],
        index='AC'
    )

    tb.Label(settings, text="Execution Settings", font=("Segoe UI", 12, "bold")).pack(pady=(15, 5))

    time_limit_var = add_combobox_row(
        settings,
        "Time Limit Per Batch (s):",
        [1, 2, 3, 5, 8, 10, 15, 30],
        SETTINGS['Time_Limit_Per_Batch'],
        index='TL'
    )

    def on_close():
        overlay.destroy()
        settings.destroy()

    settings.protocol("WM_DELETE_WINDOW", on_close)
    # Close button
    tb.Button(settings, text="Close", bootstyle="secondary", command=on_close).pack(pady=20)

    

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
    topbar = tb.Frame(root)
    topbar.pack(fill="x", pady=(15, 0), padx=15)

    # Left side: API selection and key input
    frame1 = tb.Frame(topbar)
    frame1.pack(side="left", anchor="w")

    # Right side: Settings button
    settings_btn = tb.Button(topbar, text="⚙️ Advanced Settings", bootstyle="secondary", command=open_settings)
    settings_btn.pack(side="right")


    def on_model_selected(event):
        selected = type_var.get()
        SETTINGS["Last_Use"] = selected
        set_entry_placeholder(entry, "Enter API Key", SETTINGS[SETTINGS["Last_Use"]]['API_KEY'])

    type_var = tb.StringVar(value="Gemini" if SETTINGS["Last_Use"] == None else SETTINGS["Last_Use"])
    type_menu = tb.Combobox(frame1, textvariable=type_var, values=["Gemini", "Claude", "OpenAI"], width=10, bootstyle="info")
    type_menu.pack(side="left", padx=(0, 10))
    type_menu.config(state='readonly')
    type_menu.bind("<<ComboboxSelected>>", on_model_selected)

    entry = tb.Entry(frame1, width=50, bootstyle="primary")
    entry.pack(side="left")
    set_entry_placeholder(entry, "Enter API Key", SETTINGS[SETTINGS["Last_Use"]]['API_KEY'])

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
    box1_frame = tb.Frame(bottom_text_frame)
    box1_frame.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=(0, 10))

    # Create the Text box
    text_box_1 = tb.Text(box1_frame, height=17, width=30, wrap="word")
    text_box_1.config(state="disabled", background="#1e1e1e", foreground="white")
    text_box_1.pack(fill="both", expand=True)

    # Copy function
    def copy_text_box_1():
        text_box_1.config(state="normal")
        content = text_box_1.get("1.0", "end-1c")
        text_box_1.config(state="disabled")
        root.clipboard_clear()
        root.clipboard_append(content)
        root.update()
        copy_msg_label.config(text="✓ Copied to clipboard")
        root.after(2000, lambda: copy_msg_label.config(text=""))


    copy_btn_1 = tb.Button(
        box1_frame,
        text="Copy",
        width=4,
        command=copy_text_box_1,
        bootstyle="secondary-link",
    )
    copy_btn_1.place(relx=1.0, x=-3, y=3, anchor="ne") 
    copy_msg_label = tb.Label(box1_frame, text="", bootstyle="success")
    copy_msg_label.place(relx=0.5, x=0, y=5, anchor="n")

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
        lbl = tb.Label(progress_frame, text=f"⏳ {name}", bootstyle="info", font=("Segoe UI Emoji", 9))
        lbl.pack(anchor="w", padx=20)
        subtask_labels.append(lbl)


    # Submit button
    button_frame = tb.Frame(code_input_frame)
    button_frame.pack(pady=10)

    submit_btn = tb.Button(button_frame, text="Submit", command=on_submit, bootstyle="success")
    submit_btn.pack(side="left", padx=10)

    clear_btn = tb.Button(button_frame, text=" Reset ", command=reset, bootstyle="warning")
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
