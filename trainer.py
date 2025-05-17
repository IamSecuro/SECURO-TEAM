import cv2
import os
import face_recognition
import albumentations as A
import numpy as np

# === CONFIGURATION ===
image_path = "DataSet/Joshua/photo1.jpg"  # path to your original face image
output_folder = "DataSet/Joshua_augmented"  # folder where 50 images will be saved

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Load the image
image = cv2.imread(image_path)
face_locations = face_recognition.face_locations(image)

if face_locations:
    top, right, bottom, left = face_locations[0]  # Take the first detected face
    face = image[top:bottom, left:right]
    face = cv2.resize(face, (200, 200))  # Resize face for uniformity

    # Define augmentations
    transform = A.Compose([
        A.RandomBrightnessContrast(p=0.5),
        A.HorizontalFlip(p=0.5),
        A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.1, rotate_limit=20, p=0.7),
        A.GaussNoise(p=0.2),
        A.MotionBlur(p=0.2),
        A.HueSaturationValue(p=0.3),
    ])

    # Generate 50 variations
    for i in range(50):
        augmented = transform(image=face)["image"]
        filename = os.path.join(output_folder, f"aug_{i+1}.jpg")
        cv2.imwrite(filename, augmented)

    print(f"✅ Saved 50 augmented images to: {output_folder}")
else:
    print("❌ No face detected in the input image.")
