import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# === Load ALL student embeddings from ann_data folder ===
ANN_DATA_PATH = r"E:\5G Face Attendance System\ann_data"
X = []
y = []

for student_folder in os.listdir(ANN_DATA_PATH):
    if not student_folder.endswith("_embeddings.npy"):
        continue
    student_id = student_folder.split("_")[0]
    embeddings = np.load(os.path.join(ANN_DATA_PATH, student_folder))
    X.append(embeddings)
    y.extend([student_id] * len(embeddings))

X = np.vstack(X)
y = np.array(y)

# === Label encode student IDs ===
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# === Save label encoder ===
os.makedirs("models", exist_ok=True)
with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

# === Train/test split ===
X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# === Define ANN model ===
num_classes = len(np.unique(y_encoded))

model = Sequential([
    Dense(256, activation='relu', input_shape=(512,)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# === Train ===
history = model.fit(X_train, y_train,
                    validation_data=(X_val, y_val),
                    epochs=30,
                    batch_size=16)

# === Save model ===
model.save("models/face_ann_model.h5")

print("[✅] ANN model trained and saved as models/face_ann_model.h5")
print(f"[🔖] Classes: {le.classes_}")
