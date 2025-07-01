from edge_face_recognition.mlFaceEngine import register_known_faces, recognize_face
import cv2

# === Step 1: Load known faces ===
known_faces_dir = "E:/5G Face Attendance System/known faces"  # adjust path if needed
register_known_faces(known_faces_dir)

# === Step 2: Start webcam and test ===
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    name, frame = recognize_face(frame)
    if name and name != "Unknown":
        print(f"Recognized: {name}")

    cv2.imwrite("frame_output.jpg", frame)
    print("[INFO] Saved frame to frame_output.jpg")
    break  # Exit after saving one frame
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

cap.release()
# cv2.destroyAllWindows()
