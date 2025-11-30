# Windows WhatsApp Face-Lock (Python)

A lightweight Windows "App Lock" for WhatsApp using:

- Windows Management Instrumentation (WMI)
- Win32 API
- Python + Tkinter GUI
- LBPH Face Recognition (OpenCV)

## 🔒 Features
- Locks WhatsApp with face authentication
- Instant detection of WhatsApp launch using WMI
- Hides WhatsApp window until face is verified
- Prevents repeated WMI triggers and double-launch issues
- Clean popup authentication window
- Works on UWP WhatsApp (Microsoft Store version)

## 🚀 How it Works
1. WMI detects that WhatsApp has started.
2. A watcher thread hides the WhatsApp window.
3. A Tkinter face-auth popup appears.
4. If your face matches → window is restored.
5. If not → WhatsApp stays hidden.

## 📦 Setup

### Install requirements:
pip instal -r requirements.txt

### Register your Face:
python capture.py

### Run the locker
python app_lock.py