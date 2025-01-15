import tkinter as tk
from tkinter import messagebox, filedialog
from pynput.mouse import Button, Controller
from pynput import keyboard
import threading
import time
import json
import os
from PIL import Image, ImageTk

def auto_clicker():
    global current_button, click_repeats
    while auto_clicker_running:
        if unlimited_clicks.get():
            mouse.click(current_button, 1)
            time.sleep(click_interval)
        elif click_repeats > 0:
            mouse.click(current_button, 1)
            click_repeats -= 1
            time.sleep(click_interval)
            if click_repeats <= 0:
                stop_auto_clicker()
                break
        else:
            time.sleep(click_interval)

def start_auto_clicker():
    global auto_clicker_running, click_interval, auto_clicker_thread, click_repeats
    try:
        click_interval = float(entry_interval.get())
        if click_interval <= 0:
            raise ValueError
        click_repeats = int(entry_repeats.get())
        if click_repeats <= 0:
            click_repeats = 1
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for the interval and repeats.")
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
    button_map = {
        "left": Button.left,
        "right": Button.right,
        "middle": Button.middle
    }
    current_button = button_map.get(click_type.get(), Button.left)

def save_config():
    config_data = {
        "interval": entry_interval.get(),
        "hotkey": hotkey.get(),
        "click_type": click_type.get(),
        "repeats": entry_repeats.get(),
        "unlimited_clicks": unlimited_clicks.get()
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
        click_type.set(config_data.get("click_type", "left"))
        entry_repeats.delete(0, tk.END)
        entry_repeats.insert(0, config_data.get("repeats", "1"))
        unlimited_clicks.set(config_data.get("unlimited_clicks", False))
        select_button()
        messagebox.showinfo("Load Configuration", "Configuration loaded successfully!")

mouse = Controller()
click_interval = 1.0
auto_clicker_running = False
gui_is_focused = True
current_button = Button.left
click_repeats = 1

def create_gui():
    global entry_interval, entry_repeats, btn_start, btn_stop, hotkey, click_type, unlimited_clicks

    root = tk.Tk()
    root.title("Silver Track")
    root.geometry("600x650")
    root.config(bg="#222222")

    icon_path = os.path.join("icon", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    else:
        png_icon_path = os.path.join("icon", "icon.png")
        if os.path.exists(png_icon_path):
            img = Image.open(png_icon_path)
            tk_img = ImageTk.PhotoImage(img)
            root.tk.call('wm', 'iconphoto', root._w, tk_img)

    root.bind("<FocusIn>", on_focus_in)
    root.bind("<FocusOut>", on_focus_out)

    label_title = tk.Label(root, text="Silver Track Auto-Clicker", font=("Segoe UI", 14, "bold"), fg="#a6e0a1", bg="#222222")
    label_title.pack(pady=10)

    label_interval = tk.Label(root, text="Click Interval (seconds):", fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11))
    label_interval.pack(pady=5)
    entry_interval = tk.Entry(root, font=("Segoe UI", 11), bd=2, relief="solid", highlightthickness=1, highlightcolor="#4CAF50", bg="#333333", fg="white", width=15)
    entry_interval.pack(pady=5)

    label_repeats = tk.Label(root, text="Click Repeats (per activation):", fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11))
    label_repeats.pack(pady=5)
    entry_repeats = tk.Entry(root, font=("Segoe UI", 11), bd=2, relief="solid", highlightthickness=1, highlightcolor="#4CAF50", bg="#333333", fg="white", width=15)
    entry_repeats.insert(0, "1")
    entry_repeats.pack(pady=5)

    unlimited_clicks = tk.BooleanVar(value=False)
    chk_unlimited = tk.Checkbutton(root, text="Unlimited Clicks", variable=unlimited_clicks, fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11), selectcolor="#333333")
    chk_unlimited.pack(pady=5)

    label_hotkey = tk.Label(root, text="Hotkey to Toggle:", fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11))
    label_hotkey.pack(pady=5)
    hotkey = tk.Entry(root, font=("Segoe UI", 11), bd=2, relief="solid", highlightthickness=1, highlightcolor="#4CAF50", bg="#333333", fg="white", width=15)
    hotkey.insert(0, "q")
    hotkey.pack(pady=5)

    label_button = tk.Label(root, text="Select Mouse Button:", fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11))
    label_button.pack(pady=5)

    click_type = tk.StringVar(value="left")
    click_type.trace_add("write", lambda *args: select_button())

    checkbox_left = tk.Radiobutton(root, text="Left Click", variable=click_type, value="left", fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11), selectcolor="#222222")
    checkbox_left.pack(anchor="center", pady=2)

    checkbox_right = tk.Radiobutton(root, text="Right Click", variable=click_type, value="right", fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11), selectcolor="#222222")
    checkbox_right.pack(anchor="center", pady=2)

    checkbox_middle = tk.Radiobutton(root, text="Middle Click", variable=click_type, value="middle", fg="#a6e0a1", bg="#222222", font=("Segoe UI", 11), selectcolor="#222222")
    checkbox_middle.pack(anchor="center", pady=2)

    btn_start = tk.Button(root, text="Start", command=start_auto_clicker, fg="white", bg="#4CAF50", font=("Segoe UI", 11), relief="flat", width=12, height=1)
    btn_start.pack(pady=10)

    btn_stop = tk.Button(root, text="Stop", command=stop_auto_clicker, fg="white", bg="#333333", font=("Segoe UI", 11), relief="flat", width=12, height=1, state=tk.DISABLED)
    btn_stop.pack(pady=5)

    config_frame = tk.Frame(root, bg="#222222")
    btn_save = tk.Button(config_frame, text="Save Config", command=save_config, fg="white", bg="#4CAF50", font=("Segoe UI", 11), relief="flat", width=10, height=1)
    btn_load = tk.Button(config_frame, text="Load Config", command=load_config, fg="white", bg="#4CAF50", font=("Segoe UI", 11), relief="flat", width=10, height=1)

    btn_save.grid(row=0, column=0, padx=5, pady=5)
    btn_load.grid(row=0, column=1, padx=5, pady=5)
    config_frame.pack(pady=10)

    def on_close():
        messagebox.showinfo("Closing Silver Track", "Closing Silver Track")
        stop_auto_clicker()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    listener = keyboard.Listener(on_press=on_key_press)
    listener.daemon = True
    listener.start()

    root.mainloop()

create_gui()
