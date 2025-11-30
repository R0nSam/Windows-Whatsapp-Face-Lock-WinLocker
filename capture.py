import cv2
import os
import re

os.makedirs("dataset", exist_ok=True)

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def extract_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (200, 200))
    face = cv2.equalizeHist(face)
    return face

def get_last_index():
    files = os.listdir("dataset")
    numbers = []

    for f in files:
        match = re.match(r"user\.1\.(\d+)\.jpg", f)
        if match:
            numbers.append(int(match.group(1)))

    return max(numbers) if numbers else 0

cap = cv2.VideoCapture(0)
user_id = 1

start_index = get_last_index()
count = start_index

print(f"Starting from image {count+1}...")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    face = extract_face(frame)
    if face is not None:
        count += 1
        file_path = f"dataset/user.{user_id}.{count}.jpg"
        cv2.imwrite(file_path, face)

        cv2.putText(face, str(count), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2)
        cv2.imshow("Capturing Faces", face)

    if cv2.waitKey(1) == 13 or count >= start_index + 50:
        break

cap.release()
cv2.destroyAllWindows()

print("Face capture complete.")
