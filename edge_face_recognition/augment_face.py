import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import random

# === CONFIG ===
INPUT_IMAGE_PATH = r"E:\5G Face Attendance System\test-data\student_faces\58901\58901_Arpit_Kaushik.jpg"
OUTPUT_DIR = r"E:\5G Face Attendance System\augmented_faces\58901"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === AUGMENTATION FUNCTIONS ===
def random_rotate(img):
    angle = random.choice([-20, -10, 0, 10, 20])
    return img.rotate(angle)

def change_brightness(img):
    factor = random.uniform(0.5, 1.5)
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

def add_noise(img):
    arr = np.array(img)
    noise = np.random.normal(0, 25, arr.shape).astype(np.uint8)
    noisy = cv2.add(arr, noise)
    return Image.fromarray(noisy)

def apply_blur(img):
    return img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 1.5)))

def horizontal_flip(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)

# === MAIN AUGMENTATION LOOP ===
original = Image.open(INPUT_IMAGE_PATH).convert("RGB")
augmentations = [random_rotate, change_brightness, add_noise, apply_blur, horizontal_flip]

# Save original first
original.save(os.path.join(OUTPUT_DIR, "original.jpg"))

# Generate 20 augmented samples
for i in range(1, 21):
    img = original.copy()
    for func in random.sample(augmentations, k=random.randint(1, 3)):
        img = func(img)
    img.save(os.path.join(OUTPUT_DIR, f"aug_{i}.jpg"))

print("[SUCCESS] 20 augmented images saved to:", OUTPUT_DIR)
