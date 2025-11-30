import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time

MODEL_PATH = "trainer/lbph_latest.yml"
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

CONFIDENCE_THRESHOLD = 60
REQUIRED_FRAMES = 2


def show_overlay(timeout=5):
    """
    Shows face authentication popup with camera feed.
    Returns True if face match, False otherwise.
    """

    # LOAD MODEL
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)
    cascade = cv2.CascadeClassifier(CASCADE_PATH)

    # CAMERA SETUP
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    positive = 0
    start = time.time()
    auth_result = False

    # TKINTER WINDOW
    win = tk.Tk()
    win.title("Authenticating")
    win.geometry("420x500")
    win.resizable(False, False)
    win.overrideredirect(True)
    win.attributes("-topmost", True)

    # Center popup
    win.update_idletasks()
    x = (win.winfo_screenwidth() - 420) // 2
    y = (win.winfo_screenheight() - 500) // 3
    win.geometry(f"+{x}+{y}")

    msg = tk.Label(win, text="Authenticating...", font=("Segoe UI", 16))
    msg.pack(pady=10)

    panel = tk.Label(win)
    panel.pack()

    # ------------------------  
    # UPDATE LOOP  
    # ------------------------

    def update_frame():
        nonlocal positive
        nonlocal auth_result

        ret, frame = cam.read()
        if not ret:
            win.after(10, update_frame)
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 5)

        matched = False

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            roi = cv2.equalizeHist(roi)

            _, conf = recognizer.predict(roi)
            print("confidence:", conf)

            if conf < CONFIDENCE_THRESHOLD:
                matched = True

            # Draw UI face box
            color = (0, 255, 0) if conf < CONFIDENCE_THRESHOLD else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        if matched:
            positive += 1
        else:
            positive = 0

        # Convert to Tkinter image
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        panel.imgtk = imgtk
        panel.configure(image=imgtk)

        # SUCCESS
        if positive >= REQUIRED_FRAMES:
            msg.config(text="✔ Access Granted", fg="green")
            win.update()
            auth_result = True
            time.sleep(0.5)
            cam.release()
            win.destroy()
            return

        # TIMEOUT FAIL
        if time.time() - start > timeout:
            msg.config(text="❌ Access Denied", fg="red")
            win.update()
            auth_result = False
            time.sleep(0.7)
            cam.release()
            win.destroy()
            return

        win.after(10, update_frame)

    update_frame()
    win.mainloop()

    return auth_result
