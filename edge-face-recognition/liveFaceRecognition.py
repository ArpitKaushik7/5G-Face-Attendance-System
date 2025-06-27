import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime

# Load known faces
known_face_encodings = []
known_face_names = []

known_dir = r"E:\5G Face Attendance System\known faces"
for file in os.listdir(known_dir):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        img_path = os.path.join(known_dir, file)
        img = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(file.rsplit('.', 1)[0])

# Stream from phone camera (IP Webcam app)
cap = cv2.VideoCapture(0) # Update to your stream IP

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for encoding, location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, encoding)
        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_face_names[index]

        # Draw box and label
        top, right, bottom, left = [v * 4 for v in location]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Print recognition event
        print(f"{name} recognized at {datetime.now().strftime('%H:%M:%S')}")

    cv2.imshow("Live Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
