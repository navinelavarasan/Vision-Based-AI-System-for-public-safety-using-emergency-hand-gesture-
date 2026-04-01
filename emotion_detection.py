import cv2
from deepface import DeepFace
import time

# Open camera
cap = cv2.VideoCapture(0)

last_analysis_time = 0
analysis_interval = 1.5  # seconds (to reduce lag)
current_emotion = "Detecting..."

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    current_time = time.time()
    if current_time - last_analysis_time > analysis_interval:
        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )
            current_emotion = result[0]["dominant_emotion"].upper()
        except Exception:
            current_emotion = "UNKNOWN"

        last_analysis_time = current_time

    cv2.putText(
        frame,
        f"Emotion: {current_emotion}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    if current_emotion in ["FEAR", "ANGRY", "SAD"]:
        cv2.putText(
            frame,
            "PANIC DETECTED!",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.imshow("Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

