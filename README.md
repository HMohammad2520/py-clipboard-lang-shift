# 📋 Clipboard Lang Shifter

**Automatically fix mis-typed text between languages with a single hotkey!**

This tool detects if your clipboard text is in the wrong keyboard layout (e.g., Persian typed in English or vice versa) and converts it instantly.

#### 😢 Only For Windows Users !

<br>

## 🔧 Requirements
- Python 3.7+ with tkinter option
- pip (Python package manager)
- venv (recommended for isolation)
- Internet connection (first run only, for dependency installation)

<br>

## Installation & Setup Methods

### 1. Easy Start with Git
```bat
git clone https://github.com/HMohammad2520/py-clipboard-lang-shifter.git
cd py-clipboard-lang-shifter\clipboard_lang_shifter
.\install.bat
```

### 2. Download Install
- Download a release and start `clipboard_lang_shifter\install.bat`

<br>

**`install.bat` will do the following:**
- Create virtual environment 
- Install dependencies
- Create task in taskschaduler
- Run the application

<br>

## 🎯 Features

**✔ Hotkey support** – Fix text with Ctrl+R (clipboard) or Ctrl+Alt+R (full selection) <br>
**✔ Auto-detect language direction** – Converts Persian↔English (or custom mappings) <br>
**✔ System tray icon** – Runs in background for quick access <br>
**✔ Editable layout** – Modify key mappings via the GUI <br>

<br>

## ⚡ Usage

1. Copy text (or select text in any app).
2. Press:
    - Ctrl+R → Fixes clipboard text.
    - Ctrl+Alt+R → Selects all, fixes, and pastes back.
3. Done! The text is now corrected.

<br>

## 🛠 Customizing Layouts
Open the **Edit Layout** option from the system tray to:
- Add/remove key mappings
- Save & reload changes

<br>

## Notes:
- First run will download dependencies (keyboard, pystray, plyer, etc.).
- Runs silently in the background (check system tray).

**🌟 Enjoy hassle-free multilingual typing!**

Feel free to fork the repo and contrebute
