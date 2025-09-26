import os
import numpy as np
import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# === PATHS ===
DATA_DIR = '/home/user/5G-Face-Attendance-System/ann_data'
MODEL_PATH = '/home/user/5G-Face-Attendance-System/models/ann_model.joblib'
ENCODER_PATH = '/home/user/5G-Face-Attendance-System/models/label_encoder.joblib'

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# === Load all embeddings and labels ===
X = []
y = []

for file in os.listdir(DATA_DIR):
    if file.endswith(".npy"):
        student_id = file.split("_")[0]  # e.g., 58901
        embeddings = np.load(os.path.join(DATA_DIR, file))  # shape: (N, 512)
        for emb in embeddings:
            X.append(emb)
            y.append(student_id)

X = np.array(X)
y = np.array(y)

print(f"[INFO] Total embeddings: {len(X)}, unique students: {len(set(y))}")

# === Encode labels ===
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# === Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# === Train ANN ===
clf = MLPClassifier(hidden_layer_sizes=(256, 128), max_iter=500, random_state=42)
clf.fit(X_train, y_train)

# === Evaluate ===
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {acc:.2f}")

# === Save model and encoder ===
joblib.dump(clf, MODEL_PATH)
joblib.dump(label_encoder, ENCODER_PATH)
print(f"Model saved to {MODEL_PATH}")
print(f"Label encoder saved to {ENCODER_PATH}")
