import cv2
import numpy as np
import os
from PIL import Image
from datetime import datetime

# Ensure trainer directory exists
os.makedirs("trainer", exist_ok=True)

dataset_path = "dataset"

# LBPH with better settings for small datasets
recognizer = cv2.face.LBPHFaceRecognizer_create(
    radius=2,
    neighbors=8,
    grid_x=8,
    grid_y=8
)

def load_images(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []

    for img_path in image_paths:
        img = Image.open(img_path).convert("L")  # grayscale
        img = img.resize((200, 200))             # normalize size
        img = np.array(img, "uint8")

        id_num = int(os.path.split(img_path)[-1].split(".")[1])
        face_samples.append(img)
        ids.append(id_num)

    return face_samples, ids

print("Training recognizer...")

faces, ids = load_images(dataset_path)
recognizer.train(faces, np.array(ids))

# --------------------------
# Save model with timestamp (backup)
# --------------------------
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
timestamped_path = f"trainer/lbph_{timestamp}.yml"
recognizer.write(timestamped_path)

# --------------------------
# Save/overwrite the latest model
# --------------------------
latest_path = "trainer/lbph_latest.yml"
recognizer.write(latest_path)

print(f"Training complete!\n"
      f"- Backup model saved as: {timestamped_path}\n"
      f"- Latest model saved as: {latest_path}")
