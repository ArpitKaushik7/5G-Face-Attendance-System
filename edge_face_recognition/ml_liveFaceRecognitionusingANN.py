import os
import cv2
import numpy as np
from insightface.app import FaceAnalysis
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import pickle
import datetime
import psycopg2
from sync_excel import get_student_details, load_excel

# === CONFIGURATION ===
MODEL_PATH = r"E:\5G Face Attendance System\edge_face_recognition\models\face_ann_model.h5"
LABEL_ENCODER_PATH = r"E:\5G Face Attendance System\edge_face_recognition\models\label_encoder.pkl"
DB_CONFIG = {
    "dbname": "attendance_db",
    "user": "admin",
    "password": "Kaushikjii@7",
    "host": "localhost",
    "port": 5432,
}
SUBJECT = "AI/ML"
LECTURE_SLOT = "10:00 AM - 11:00 AM"

# === LOAD ===
model = load_model(MODEL_PATH)
with open(LABEL_ENCODER_PATH, "rb") as f:
    le: LabelEncoder = pickle.load(f)

face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

df = load_excel()

# ✅ Track attendance already marked
marked_ids = set()

cap = cv2.VideoCapture(0)
print("[INFO] Scanning...")

marked_times = {}
TIME_LIMIT_MINUTES = 60

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = datetime.datetime.now()
    date_str = now.date()
    time_str = now.time()

    faces = face_app.get(frame)
    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)
        face_embedding = face.embedding.reshape(1, -1)

        predictions = model.predict(face_embedding)
        predicted_class = np.argmax(predictions)
        confidence = predictions[0][predicted_class]

        name_display = "Unknown"

        if confidence >= 0.8:
            predicted_id = str(le.inverse_transform([predicted_class])[0])
            key = (predicted_id, SUBJECT, LECTURE_SLOT)

            try:
                last_marked = marked_times.get(key)
                if last_marked is None or (now - last_marked).total_seconds() >= TIME_LIMIT_MINUTES * 60:
                    conn = psycopg2.connect(**DB_CONFIG)
                    cursor = conn.cursor()

                    name, branch, batch = get_student_details(predicted_id, df)
                    predicted_id = str(le.inverse_transform([predicted_class])[0])

                    name = str(name)
                    branch = str(branch)
                    batch = str(batch)
                    date_str = now.date().isoformat()
                    time_str = now.time().strftime('%H:%M:%S')

                    cursor.execute("""
                    INSERT INTO attendance_logs (id, date, time, name, branch, batch, subject, lecture_slot)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (predicted_id, date_str, time_str, name, branch, batch, SUBJECT, LECTURE_SLOT))

                    conn.commit()
                    cursor.close()
                    conn.close()

                    marked_times[key] = now
                    print(f"[✅] Attendance marked for: {name} ({predicted_id})")
                    name_display = f"{name} ({predicted_id})"
                else:
                    name_display = f"{name} ({predicted_id}) [ Already Marked <1hr]"

            except Exception as e:
                print(f"[ERROR] DB issue: {e}")
                name_display = "DB Error"

        # Draw box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name_display, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Face Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
