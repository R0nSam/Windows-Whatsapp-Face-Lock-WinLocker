# watch_whatsapp.py

import wmi
import threading
import win32gui
import win32con
import time

TARGET_NAME = "whatsapp"
is_authenticating = False
window_hidden = False


def hide_once():
    """Hide WhatsApp window only ONE time."""
    global window_hidden, is_authenticating

    print("[i] Waiting for WhatsApp window...")

    while is_authenticating and not window_hidden:
        def callback(hwnd, _):
            global window_hidden
            title = win32gui.GetWindowText(hwnd).lower()

            if TARGET_NAME in title and not window_hidden:
                print("[+] WhatsApp window found. Hiding ONCE.")
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                window_hidden = True  # stop future hiding
            return True

        win32gui.EnumWindows(callback, None)
        time.sleep(0.05)  # check 20 fps

    print("[i] hide_once thread exiting.")


def monitor_whatsapp(on_detect_callback):
    global is_authenticating, window_hidden

    c = wmi.WMI()
    watcher = c.Win32_Process.watch_for("creation")

    print("[i] Watching for WhatsApp...")

    while True:
        process = watcher()
        exe = process.Caption.lower()

        if TARGET_NAME in exe:
            if is_authenticating:
                print("[i] Ignoring duplicate launch.")
                continue

            print(f"[+] WhatsApp detected: {exe}")

            # mark auth start
            is_authenticating = True
            window_hidden = False

            # start hide-once watcher
            threading.Thread(target=hide_once, daemon=True).start()

            # begin face authentication
            on_detect_callback()

            # stop any further hiding
            is_authenticating = False
            print("[i] Authentication cycle complete. No more hiding.")
