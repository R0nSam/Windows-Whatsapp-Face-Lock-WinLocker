# app_lock.py

from watch_whatsapp import monitor_whatsapp, TARGET_NAME
from face_window import show_overlay
import win32gui
import win32con
import time


def unhide_whatsapp():
    """Restore WhatsApp only once."""
    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd).lower()

        if TARGET_NAME in title:
            print("[i] Restoring WhatsApp...")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        return True

    win32gui.EnumWindows(callback, None)


def on_whatsapp_launched():
    print("[i] Starting Face Authentication...")

    result = show_overlay(timeout=5)

    if result:
        print("[+] Face Verified — Restoring WhatsApp")
        unhide_whatsapp()
        time.sleep(1)
    else:
        print("[!] Access Denied")
        # WhatsApp remains hidden


if __name__ == "__main__":
    monitor_whatsapp(on_whatsapp_launched)
