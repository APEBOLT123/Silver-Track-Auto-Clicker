import tkinter as tk
from tkinter import messagebox, filedialog
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
import time
import pyfiglet
import sys
import os
import json

def display_ascii_banner():
    ascii_art = pyfiglet.figlet_format("Silver Track")
    print(f"\033[92m{ascii_art}\033[0m")

def auto_clicker():
    while auto_clicker_running:
        if not gui_is_focused:
            mouse.click(current_button, 1)
        time.sleep(click_interval)

def start_auto_clicker():
    global auto_clicker_running, click_interval, auto_clicker_thread, current_button
    try:
        click_interval = float(entry_interval.get())
        if click_interval <= 0:
            raise ValueError("Interval must be positive.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number for the interval (in seconds).")
        return

    auto_clicker_running = True
    auto_clicker_thread = threading.Thread(target=auto_clicker)
    auto_clicker_thread.daemon = True
    auto_clicker_thread.start()
    btn_start.config(state=tk.DISABLED)
    btn_stop.config(state=tk.NORMAL, bg="#ff4d4d", fg="white")

def stop_auto_clicker():
    global auto_clicker_running
    auto_clicker_running = False

    btn_start.config(state=tk.NORMAL)
    btn_stop.config(state=tk.DISABLED, bg="#333333", fg="white")

def toggle_auto_clicker():
    if auto_clicker_running:
        stop_auto_clicker()
    else:
        start_auto_clicker()

def on_key_press(key):
    try:
        if key.char == hotkey.get():
            toggle_auto_clicker()
    except AttributeError:
        pass

def on_focus_in(event):
    global gui_is_focused
    gui_is_focused = True

def on_focus_out(event):
    global gui_is_focused
    gui_is_focused = False

def select_button():
    global current_button
    if check_left.get():
        current_button = Button.left
    elif check_right.get():
        current_button = Button.right
    elif check_middle.get():
        current_button = Button.middle

def save_config():
    config_data = {
        "interval": entry_interval.get(),
        "hotkey": hotkey.get(),
        "left_click": check_left.get(),
        "right_click": check_right.get(),
        "middle_click": check_middle.get()
    }

    if not os.path.exists("cfgs"):
        os.makedirs("cfgs")

    filepath = filedialog.asksaveasfilename(initialdir="cfgs", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filepath:
        with open(filepath, "w") as f:
            json.dump(config_data, f)
        messagebox.showinfo("Save Configuration", "Configuration saved successfully!")

def load_config():
    filepath = filedialog.askopenfilename(initialdir="cfgs", filetypes=[("JSON Files", "*.json")])
    if filepath:
        with open(filepath, "r") as f:
            config_data = json.load(f)

        entry_interval.delete(0, tk.END)
        entry_interval.insert(0, config_data.get("interval", "1.0"))
        hotkey.delete(0, tk.END)
        hotkey.insert(0, config_data.get("hotkey", "q"))
        check_left.set(config_data.get("left_click", True))
        check_right.set(config_data.get("right_click", False))
        check_middle.set(config_data.get("middle_click", False))

        select_button()
        messagebox.showinfo("Load Configuration", "Configuration loaded successfully!")

mouse = Controller()
click_interval = 1.0
auto_clicker_running = False
gui_is_focused = True
current_button = Button.left

def create_gui():
    global entry_interval, btn_start, btn_stop, hotkey, check_left, check_right, check_middle

    root = tk.Tk()
    root.title("Silver Track")
    root.geometry("800x700")
    root.config(bg="#333333")

    root.bind("<FocusIn>", on_focus_in)
    root.bind("<FocusOut>", on_focus_out)

    label_title = tk.Label(root, text="Silver Track Auto-Clicker", font=("Arial", 16), fg="lightgreen", bg="#333333")
    label_title.pack(pady=10)

    label_interval = tk.Label(root, text="Click Interval (seconds):", fg="lightgreen", bg="#333333", font=("Arial", 12))
    label_interval.pack(pady=5)
    entry_interval = tk.Entry(root, font=("Arial", 14))
    entry_interval.pack(pady=5)

    label_hotkey = tk.Label(root, text="Hotkey to Toggle:", fg="lightgreen", bg="#333333", font=("Arial", 12))
    label_hotkey.pack(pady=5)
    hotkey = tk.Entry(root, font=("Arial", 14))
    hotkey.insert(0, "q")
    hotkey.pack(pady=5)

    label_button = tk.Label(root, text="Select Mouse Button:", fg="lightgreen", bg="#333333", font=("Arial", 12))
    label_button.pack(pady=5)

    check_left = tk.BooleanVar(value=True)
    check_right = tk.BooleanVar(value=False)
    check_middle = tk.BooleanVar(value=False)

    checkbox_left = tk.Checkbutton(root, text="Left Click", variable=check_left, fg="lightgreen", bg="#333333", font=("Arial", 12), command=select_button, selectcolor="#333333")
    checkbox_left.pack(anchor="w", padx=10)
    checkbox_right = tk.Checkbutton(root, text="Right Click", variable=check_right, fg="lightgreen", bg="#333333", font=("Arial", 12), command=select_button, selectcolor="#333333")
    checkbox_right.pack(anchor="w", padx=10)
    checkbox_middle = tk.Checkbutton(root, text="Middle Click", variable=check_middle, fg="lightgreen", bg="#333333", font=("Arial", 12), command=select_button, selectcolor="#333333")
    checkbox_middle.pack(anchor="w", padx=10)

    btn_start = tk.Button(root, text="Start", command=start_auto_clicker, fg="white", bg="#228B22", font=("Arial", 14))
    btn_start.pack(pady=15)

    btn_stop = tk.Button(root, text="Stop", command=stop_auto_clicker, fg="white", bg="#333333", state=tk.DISABLED, font=("Arial", 14))
    btn_stop.pack(pady=5)

    btn_save = tk.Button(root, text="Save Config", command=save_config, fg="white", bg="#228B22", font=("Arial", 14))
    btn_save.pack(pady=5)

    btn_load = tk.Button(root, text="Load Config", command=load_config, fg="white", bg="#228B22", font=("Arial", 14))
    btn_load.pack(pady=5)

    def on_close():
        messagebox.showinfo("Closing Silver Track", "Closing Silver Track")
        stop_auto_clicker()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    listener = keyboard.Listener(on_press=on_key_press)
    listener.daemon = True
    listener.start()

    root.mainloop()

if __name__ == "__main__":
    print("\033[92mStarting Silver Track...\033[0m")
    display_ascii_banner()

    print("\033[92mStarting GUI...\033[0m")

    create_gui()

    print("\033[92mExiting Silver Track.\033[0m")
    sys.exit()
