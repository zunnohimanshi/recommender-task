import cv2
import mediapipe as mp
import math
from datetime import datetime
import os

# Initialize Mediapipe
mp_face_mesh = mp.solutions.face_mesh

# Create recordings folder if not exists
if not os.path.exists("recordings"):
    os.makedirs("recordings")

# Generate unique filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"recordings/session_{timestamp}.mp4"

# Helper functions
def calculate_head_movement(landmarks):
    left_eye = landmarks[133]
    right_eye = landmarks[362]
    dx = right_eye.x - left_eye.x
    dy = right_eye.y - left_eye.y
    angle = math.degrees(math.atan2(dy, dx))
    return angle

def detect_eye_movement(landmarks):
    left_iris_y = landmarks[159].y
    left_iris_lower_y = landmarks[145].y
    return left_iris_lower_y - left_iris_y

# Start webcam
cap = cv2.VideoCapture(0)

# Get resolution
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Configure writer (macOS compatible codec)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

print(f"[INFO] Recording session started. Saving to: {output_path}")

with mp_face_mesh.FaceMesh(static_image_mode=False,
                           max_num_faces=1,
                           refine_landmarks=True,
                           min_detection_confidence=0.7,
                           min_tracking_confidence=0.7) as face_mesh:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("[ERROR] Cannot access webcam.")
            break

        frame = cv2.flip(frame, 1)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_image)

        if result.multi_face_landmarks:
            for face_landmarks in result.multi_face_landmarks:
                landmarks = face_landmarks.landmark

                # Head angle
                angle = calculate_head_movement(landmarks)
                if angle > 15:
                    direction = "Looking Right"
                    warning = "⚠️ Turned Right - Stay Focused"
                    color = (0, 0, 255)
                elif angle < -15:
                    direction = "Looking Left"
                    warning = "⚠️ Turned Left - Stay Focused"
                    color = (0, 0, 255)
                elif 5 < angle <= 15 or -15 <= angle < -5:
                    direction = "Slight Head Movement"
                    warning = "⚠️ Suspicious Slight Movement"
                    color = (0, 165, 255)
                else:
                    direction = "Looking Center"
                    warning = ""
                    color = (0, 255, 0)

                # Eye state
                eye_movement = detect_eye_movement(landmarks)
                if eye_movement < 0.01:
                    eye_status = "⚠️ Eyes Closed / Down"
                else:
                    eye_status = "Eyes Open"

                # Display data
                cv2.putText(frame, f"Head Angle: {angle:.2f}", (20, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(frame, direction, (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(frame, eye_status, (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)

                if warning:
                    cv2.putText(frame, warning, (20, 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "❌ No Face Detected", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Show and record
        cv2.imshow("📹 Proctoring - Face & Eye Tracker", frame)
        out.write(frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            print("[INFO] Session ended.")
            break

# Clean up
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"[INFO] Video saved at: {output_path}")
