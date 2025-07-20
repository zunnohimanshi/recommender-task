import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)
print("[INFO] Starting webcam... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("[ERROR] Cannot read frame from webcam.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)
        status = "Face Detected"
        color = (0, 255, 0)
    else:
        status = "No Face"
        color = (0, 0, 255)

    cv2.putText(frame, status, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Proctoring Window", frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
