import os
import json
import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from pystray import Icon, MenuItem as Item, Menu
from PIL import Image, ImageDraw
import keyboard
import pyperclip
from plyer import notification

CONFIG_FILE = 'layout.json'
layout_map = {}

# ------------------ Config Handling ------------------

def load_layout():
    global layout_map
    layout_map.clear()

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        layout_map.update(json.load(f))

def save_layout():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(layout_map, f, ensure_ascii=False, indent=2)

# ------------------ Conversion ------------------

def convert_text(text):
    persian_chars = sum(1 for c in text if '؀' <= c <= 'ۿ' or 'ݐ' <= c <= 'ݿ')
    ascii_chars = sum(1 for c in text if ' ' <= c <= '~')
    direction = 'FA_TO_EN' if persian_chars > ascii_chars else 'EN_TO_FA'
    output = ''
    i = 0
    if direction == 'EN_TO_FA':
        mapping = layout_map
    else:
        mapping = {v: k for k, v in layout_map.items() if list(layout_map.values()).count(v) == 1}

    max_key_len = max((len(k) for k in mapping), default=1)
    while i < len(text):
        matched = False
        for l in range(min(max_key_len, len(text) - i), 0, -1):
            segment = text[i:i+l]
            if segment in mapping:
                output += mapping[segment]
                i += l
                matched = True
                break
        if not matched:
            output += text[i]
            i += 1
    return output

# ------------------ Notifications ------------------

def notify(msg):
    notification.notify(title='Layout Fixer', message=msg, timeout=2)

# ------------------ Clipboard ------------------

def fix_clipboard():
    text = pyperclip.paste()
    fixed = convert_text(text)
    pyperclip.copy(fixed)
    notify("Clipboard fixed")

def no_keys_pressed():
    return len(keyboard._pressed_events) == 0

def wait_no_keypress(timeout):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not no_keys_pressed():
            time.sleep(0.2)
        else:
            # All keys released, perform the action
            keyboard.press_and_release('alt+shift')
            break
    
def shortcut_simple_pressed():
    fix_clipboard()
    wait_no_keypress(3)
    keyboard.press_and_release('alt+shift')

def shortcut_full_pressed():
    wait_no_keypress(3)
    keyboard.press_and_release('ctrl+a'); time.sleep(0.01)

    wait_no_keypress(3)
    keyboard.press_and_release('ctrl+x'); time.sleep(0.01)
    fix_clipboard()

    wait_no_keypress(3)
    keyboard.press_and_release('ctrl+v'); time.sleep(0.01)
    
    wait_no_keypress(3)
    keyboard.press_and_release('alt+shift'); time.sleep(0.01)

# ------------------ Edit Layout UI ------------------

def edit_layout_gui():
    def refresh_list():
        listbox.delete(0, tk.END)
        for k, v in layout_map.items():
            listbox.insert(tk.END, f"{k} ↔ {v}")

    def add_mapping():
        k = key_entry.get().strip()
        v = val_entry.get().strip()
        if k and v:
            layout_map[k] = v
            key_entry.delete(0, tk.END)
            val_entry.delete(0, tk.END)
            refresh_list()
        else:
            messagebox.showwarning("Input Error", "Both fields must be filled.")

    def remove_selected():
        try:
            selected = listbox.get(listbox.curselection())
            k = selected.split(" ↔ ")[0]
            del layout_map[k]
            refresh_list()
        except:
            pass

    def save_and_reload():
        save_layout()
        load_layout()
        notify("Layout saved & reloaded")
        win.destroy()

    win = tk.Tk()
    win.title("Edit Layout")
    win.geometry("420x460")
    win.resizable(False, False)

    # Use ttk for cleaner widgets
    style = ttk.Style(win)
    style.theme_use('clam')

    frm_top = ttk.LabelFrame(win, text="Add Mapping")
    frm_top.pack(padx=10, pady=10, fill='x')

    key_label = ttk.Label(frm_top, text="Key:")
    key_label.grid(row=0, column=0, padx=(10, 2), pady=8, sticky="e")
    key_entry = ttk.Entry(frm_top, width=10)
    key_entry.grid(row=0, column=1, padx=2, pady=8)

    val_label = ttk.Label(frm_top, text="Value:")
    val_label.grid(row=0, column=2, padx=2, pady=8, sticky="e")
    val_entry = ttk.Entry(frm_top, width=20)
    val_entry.grid(row=0, column=3, padx=2, pady=8)

    add_btn = ttk.Button(frm_top, text="Add", command=add_mapping)
    add_btn.grid(row=0, column=4, padx=(8, 10), pady=8)

    frm_list = ttk.LabelFrame(win, text="Current Mappings")
    frm_list.pack(padx=10, pady=(0, 10), fill='both', expand=True)

    list_frame = tk.Frame(frm_list)
    list_frame.pack(fill='both', expand=True)

    listbox = tk.Listbox(list_frame)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=5)

    remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=remove_selected)
    remove_btn.pack(side=tk.LEFT, padx=10)

    save_btn = ttk.Button(btn_frame, text="Save & Reload", command=save_and_reload)
    save_btn.pack(side=tk.RIGHT, padx=10)

    refresh_list()
    win.mainloop()

# ------------------ Tray ------------------

def create_icon():
    image = Image.new('RGB', (64, 64), color=(40, 40, 40))
    d = ImageDraw.Draw(image)
    d.text((10, 20), "Aa", fill=(255, 255, 255))

    menu = Menu(
        Item('Edit Layout', lambda icon, item: threading.Thread(target=edit_layout_gui, daemon=True).start()),
        Item('Quit', lambda icon, item: icon.stop())
    )
    return Icon("LayoutFixer", image, "Layout Fixer", menu)

# ------------------ Main ------------------

def main():
    load_layout()
    keyboard.add_hotkey("ctrl+r", shortcut_simple_pressed)
    keyboard.add_hotkey("ctrl+alt+r", shortcut_full_pressed)
    notify(f"Clipboard Lang Shifter is running (ctrl+r) or (ctrl+alt+r)")
    icon = create_icon()

    # Run tray icon in a separate thread
    tray_thread = threading.Thread(target=icon.run)
    tray_thread.start()

    try:
        while tray_thread.is_alive():
            tray_thread.join(0.5)
    except (KeyboardInterrupt, SystemExit):
        icon.stop()

if __name__ == '__main__':
    main()
