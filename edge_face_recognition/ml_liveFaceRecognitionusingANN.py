import os
import cv2
import numpy as np
import joblib
import datetime
import psycopg2
from insightface.app import FaceAnalysis
from sync_excel import get_student_details, load_excel

# === CONFIGURATION ===
MODEL_PATH = r"E:\5G Face Attendance System\edge_face_recognition\models\ann_model.joblib"
LABEL_ENCODER_PATH = r"E:\5G Face Attendance System\edge_face_recognition\models\label_encoder.joblib"

DB_CONFIG = {
    "dbname": "attendance_db",
    "user": "admin",
    "password": "Kaushikjii@7",
    "host": "localhost",
    "port": 5432,
}
SUBJECT = "AI/ML"
LECTURE_SLOT = "10:00 AM - 11:00 AM"

# === LOAD MODEL AND ENCODER ===
model = joblib.load(MODEL_PATH)
le = joblib.load(LABEL_ENCODER_PATH)

# === FACE ANALYSIS ===
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

df = load_excel()

marked_times = {}
TIME_LIMIT_MINUTES = 60  # Prevent double marking within 1 hour

cap = cv2.VideoCapture(0)
print("[INFO] Scanning...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    now = datetime.datetime.now()
    faces = face_app.get(frame)

    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)
        embedding = face.embedding.reshape(1, -1)

        name_display = "Unknown"

        try:
            predicted_class = model.predict(embedding)[0]
            predicted_proba = model.predict_proba(embedding)[0]
            confidence = np.max(predicted_proba)

            if confidence >= 0.8:
                predicted_id = str(le.inverse_transform([predicted_class])[0])
                key = (predicted_id, SUBJECT, LECTURE_SLOT)

                try:
                    conn = psycopg2.connect(**DB_CONFIG)
                    cursor = conn.cursor()

                    # Check for duplicate attendance in the same lecture slot within 1 hour
                    cursor.execute("""
                        SELECT time FROM attendance_logs
                        WHERE id = %s AND subject = %s AND lecture_slot = %s
                        AND date = %s
                        ORDER BY time DESC
                        LIMIT 1
                    """, (predicted_id, SUBJECT, LECTURE_SLOT, now.date()))
                    last_time_row = cursor.fetchone()

                    allow_mark = True
                    if last_time_row:
                        last_marked_time = datetime.datetime.combine(now.date(), last_time_row[0])
                        if (now - last_marked_time).total_seconds() < TIME_LIMIT_MINUTES * 60:
                            allow_mark = False

                    if allow_mark:
                        name, branch, batch = get_student_details(predicted_id, df)
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

                        marked_times[key] = now
                        print(f"[✅] Attendance marked for: {name} ({predicted_id})")
                        name_display = f"{name} ({predicted_id})"
                    else:
                        print(f"[⛔] Already marked within last 1 hour for {predicted_id}")
                        name_display = f"{predicted_id} [Already Marked <1hr]"

                    cursor.close()
                    conn.close()

                except Exception as db_err:
                    print(f"[DB ERROR] {db_err}")

        except Exception as e:
            print(f"[ERROR] Prediction failed: {e}")

        # Draw rectangle and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name_display, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Face Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
