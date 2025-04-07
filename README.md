# SnapStack

SnapStack is a lightweight window management utility that lets you snap your active windows to the top or bottom half of the screen using simple hotkeys. Designed for productivity-focused users who prefer vertical window tiling over traditional side-by-side layouts.

## Features

- Snap any active window to the top half of the screen
- Snap to the bottom half
- Customizable hotkeys (coming soon)
- Native desktop app with a clean, minimal GUI
- Lightweight and easy to install
- Built for Windows (Linux and Mac support coming soon)

## Tech Stack

- Language: Python 3.10+
- GUI: PySide6 (Qt for Python)
- Window control: pygetwindow, pywinauto
- Hotkey detection: keyboard
- Display handling: screeninfo or pywin32

## Getting Started

### Installation

1. Clone the repo:
```bash
git clone https://github.com/Dawson02/snapstack.git
cd snapstack
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
python main.py
```

## Usage

- Press **Ctrl + Alt + Up** to snap the active window to the top.
- Press **Ctrl + Alt + Down** to snap it to the bottom.

Coming soon:
- Tray icon with options
- Multi-monitor support
- Custom layouts & shortcuts

## Project Structure

```
snapstack/
│
├── main.py               # Entry point
├── snapper.py            # Logic for snapping windows
├── ui/
│   └── main_window.ui    # PySide6 UI layout
├── assets/               # Icons, logos
├── utils/
│   └── monitor_info.py   # Utility functions for screen detection
├── requirements.txt      # Dependencies
└── README.md             # You're reading it :)
```

## License

MIT License – feel free to use, modify, and distribute as long as you include credit.

## Author

Dawson Murray
