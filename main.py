import cv2
import os
import sys
import glob

MODEL_DIR = "trainer"
LATEST_MODEL = os.path.join(MODEL_DIR, "lbph_latest.yml")

FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# Recognition settings
CONFIDENCE_THRESHOLD = 55
REQUIRED_FRAMES = 5


def list_timestamped_models():
    """Return all timestamped models sorted newest → oldest."""
    models = glob.glob(os.path.join(MODEL_DIR, "lbph_*.yml"))
    models.sort(reverse=True)  # newest first
    return models


def choose_timestamp_model():
    """Interactive chooser for timestamped models."""
    models = list_timestamped_models()

    if not models:
        print("No timestamped models found in trainer/.")
        sys.exit(1)

    print("\nAvailable trained models:")
    for i, m in enumerate(models, 1):
        print(f"  {i}. {os.path.basename(m)}")

    while True:
        choice = input("\nSelect model number: ")
        if not choice.isdigit():
            print("Enter a valid number.")
            continue

        idx = int(choice)
        if 1 <= idx <= len(models):
            return models[idx - 1]
        else:
            print("Number out of range.")


def load_model(use_timestamp=False):
    """Load the LBPH model (latest or chosen)."""
    if use_timestamp:
        model_path = choose_timestamp_model()
    else:
        model_path = LATEST_MODEL

    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        sys.exit(1)

    print(f"Loading model: {model_path}")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)
    return recognizer


def main():
    # Check if user passed -t to choose timestamp model
    use_timestamp = "-t" in sys.argv

    # Load model
    recognizer = load_model(use_timestamp)

    # Load face detector
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

    # Start webcam
    cap = cv2.VideoCapture(0)
    positive_frames = 0

    print("\nRecognizer running... Press ENTER in window to exit.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        matched = False
        confidence_value = None

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200,200))
            roi = cv2.equalizeHist(roi)

            id_, confidence = recognizer.predict(roi)
            confidence_value = confidence

            if confidence < CONFIDENCE_THRESHOLD:
                text = f"Match ({confidence:.1f})"
                color = (0,255,0)
                matched = True
            else:
                text = f"Unknown ({confidence:.1f})"
                color = (0,0,255)

            cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)
            cv2.putText(frame, text, (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # frame counting logic
        if matched:
            positive_frames += 1
        else:
            positive_frames = 0

        cv2.putText(frame,
                    f"Positive: {positive_frames}/{REQUIRED_FRAMES}",
                    (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255,255,255), 2)

        cv2.imshow("Face Recognition", frame)

        if positive_frames >= REQUIRED_FRAMES:
            print("\n### ACCESS GRANTED ###\n")
            positive_frames = 0

        if cv2.waitKey(1) == 13:  # Enter to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
