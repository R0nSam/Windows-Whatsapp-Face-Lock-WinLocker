import cv2
import os
import time

MODEL_PATH = "trainer/lbph_latest.yml"
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

CONFIDENCE_THRESHOLD = 60        # based on your tests
REQUIRED_FRAMES = 2              # small for quick unlock


def load_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)
    return recognizer


def verify_face(timeout=5):
    recognizer = load_model()
    cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    positive = 0
    start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 5)

        matched = False

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200,200))
            roi = cv2.equalizeHist(roi)

            _, conf = recognizer.predict(roi)

            # print raw values for debugging
            print("confidence:", conf)

            if conf < CONFIDENCE_THRESHOLD:
                matched = True

        if matched:
            positive += 1
        else:
            positive = 0

        # success
        if positive >= REQUIRED_FRAMES:
            cap.release()
            return True

        # timeout
        if time.time() - start > timeout:
            cap.release()
            return False
