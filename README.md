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

## 📂 Directory Structure
After cloning this repo, make sure your directory has the following structure
Winlocker/
|
|——dataset
|——trainer
|——<rest of the python files>
It is recommended to create the folders dataset and trainer.

#### Having a virtual environment will be safer.

### Install requirements:
pip instal -r requirements.txt

### Register your Face:
python capture.py
It is recommended to capture your face multiple times in different lighting/angles/environemnts. If you wear glasses, capture both with and without glasses.

### Train the Model
python train.py
I have used OpenCV LPBH as the model. It's a lightweight face recognition algorithm that doesnot need GPU.

### Run the locker
python app_lock.py

## ⚠️ Disclaimer
This project is only intended for learning and experimenting. Face lock is not 100% secure. More features will be added in the future.