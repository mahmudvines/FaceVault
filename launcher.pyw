"""
FaceVault Silent Launcher
- .pyw extension = Python runs with no console window on Windows
- Starts Flask in a background thread
- Opens browser automatically
- Adds a system tray icon to quit cleanly
"""
import sys
import os
import threading
import time
import webbrowser
import subprocess
import tkinter as tk
from tkinter import messagebox

# ── Make sure we run from the script's own directory ──────────────────────────
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 5050
URL  = f"http://localhost:{PORT}"

# ── Check dependencies silently before starting ───────────────────────────────
def check_and_install():
    required = ["flask", "PIL", "numpy", "tqdm"]
    missing  = []
    for pkg in required:
        try:
            __import__(pkg if pkg != "PIL" else "PIL.Image")
        except ImportError:
            missing.append(pkg)

    if missing:
        # Show a simple install dialog
        root = tk.Tk()
        root.withdraw()
        go = messagebox.askyesno(
            "FaceVault — First Run",
            f"Some packages need to be installed:\n{', '.join(missing)}\n\nInstall now? (takes ~1 min)"
        )
        root.destroy()
        if not go:
            sys.exit(0)

        # Install silently
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "flask", "pillow", "numpy", "tqdm", "--quiet"],
            creationflags=0x08000000  # CREATE_NO_WINDOW
        )

    # face_recognition check separately (heavier)
    try:
        import face_recognition
    except ImportError:
        root = tk.Tk()
        root.withdraw()
        go = messagebox.askyesno(
            "FaceVault — face_recognition",
            "face_recognition is not installed.\nThis enables face detection.\n\nInstall now? (may take 3-5 minutes)"
        )
        root.destroy()
        if go:
            subprocess.call(
                [sys.executable, "-m", "pip", "install", "face_recognition", "--quiet"],
                creationflags=0x08000000
            )

# ── Start Flask in a daemon thread ────────────────────────────────────────────
def start_flask():
    # Suppress Flask output
    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)

    # Import and run the app
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from app import app
    app.run(host="127.0.0.1", port=PORT, debug=False, use_reloader=False)

# ── Tray icon using tkinter (no extra libs needed) ────────────────────────────
class TrayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # hide main window

        # Small always-on-top status window
        self.status = tk.Toplevel(self.root)
        self.status.title("FaceVault")
        self.status.geometry("260x90")
        self.status.resizable(False, False)
        self.status.configure(bg="#090b10")
        self.status.attributes("-topmost", True)
        self.status.protocol("WM_DELETE_WINDOW", self.quit_app)

        # Position bottom-right
        sw = self.status.winfo_screenwidth()
        sh = self.status.winfo_screenheight()
        self.status.geometry(f"260x90+{sw-280}+{sh-120}")

        # UI
        tk.Label(
            self.status, text="👁  FaceVault",
            fg="#00e5ff", bg="#090b10",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(12, 0))

        tk.Label(
            self.status, text="Running at localhost:5050",
            fg="#5a6478", bg="#090b10",
            font=("Segoe UI", 8)
        ).pack()

        btn_frame = tk.Frame(self.status, bg="#090b10")
        btn_frame.pack(pady=8)

        tk.Button(
            btn_frame, text="Open Browser",
            command=self.open_browser,
            bg="#00e5ff", fg="#000000",
            font=("Segoe UI", 8, "bold"),
            relief="flat", padx=10, pady=4, cursor="hand2"
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Quit",
            command=self.quit_app,
            bg="#1e2535", fg="#ff4060",
            font=("Segoe UI", 8),
            relief="flat", padx=10, pady=4, cursor="hand2"
        ).pack(side="left", padx=4)

    def open_browser(self):
        webbrowser.open(URL)

    def quit_app(self):
        if messagebox.askokcancel("FaceVault", "Stop FaceVault?"):
            self.root.destroy()
            os._exit(0)

    def run(self):
        self.root.mainloop()

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 1. Check/install deps
    check_and_install()

    # 2. Start Flask silently in background
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # 3. Wait for Flask to be ready, then open browser
    def delayed_open():
        time.sleep(1.5)
        webbrowser.open(URL)

    threading.Thread(target=delayed_open, daemon=True).start()

    # 4. Show small tray-style status window & run event loop
    app = TrayApp()
    app.run()
