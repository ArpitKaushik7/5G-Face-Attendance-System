import os
import numpy as np
import cv2
from insightface.app import FaceAnalysis

# === PATHS ===
INPUT_DIR = r"E:\5G Face Attendance System\augmented_faces"
OUTPUT_DIR = r"E:\5G Face Attendance System\ann_data"

# === Initialize FaceAnalysis ===
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# === Create output folder if not exists ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Loop through each student folder ===
for student_id in os.listdir(INPUT_DIR):
    student_path = os.path.join(INPUT_DIR, student_id)
    if not os.path.isdir(student_path):
        continue

    embeddings = []

    print(f"[INFO] Processing student: {student_id}")

    for file in os.listdir(student_path):
        img_path = os.path.join(student_path, file)

        # Read and process image
        img = cv2.imread(img_path)
        if img is None:
            print(f"[WARN] Failed to read image: {img_path}")
            continue

        faces = app.get(img)
        if not faces:
            print(f"[WARN] No face found in {img_path}")
            continue

        # Take first face
        embedding = faces[0].embedding
        embeddings.append(embedding)

    if embeddings:
        embeddings_array = np.array(embeddings)
        np.save(os.path.join(OUTPUT_DIR, f"{student_id}_embeddings.npy"), embeddings_array)
        print(f"[✅] Saved embeddings for {student_id}, shape: {embeddings_array.shape}")
    else:
        print(f"[❌] No valid embeddings found for {student_id}")

print("\n[✅] Embedding generation completed for all students.")
