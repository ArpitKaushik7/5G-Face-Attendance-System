import cv2

cap = cv2.VideoCapture("rtsp://admin:admin123@10.45.0.201:554/avstream/channel=<1>/stream=<0-mainstream;1-substream>.sdp")

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
