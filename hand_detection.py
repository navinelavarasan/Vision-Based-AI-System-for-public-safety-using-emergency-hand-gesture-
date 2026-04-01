import cv2
import mediapipe as mp
import time
import os
from datetime import datetime
from email_alert import send_email_alert

# ================== SETTINGS ==================
PANIC_TIME = 5   # ✅ 5 seconds to confirm emergency
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ================== MEDIAPIPE SETUP ==================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ================== VARIABLES ==================
panic_start_time = None
emergency_confirmed = False
screenshot_taken = False

# ================== CAMERA ==================
cap = cv2.VideoCapture(0)

print("[INFO] Emergency Hand Detection Started")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # ================== HAND DETECTED ==================
    if result.multi_hand_landmarks:
        current_time = time.time()

        if panic_start_time is None:
            panic_start_time = current_time
            print("[INFO] Hand detected — timer started")

        elapsed = current_time - panic_start_time
        remaining = max(0, int(PANIC_TIME - elapsed))

        cv2.putText(
            frame,
            f"Hold hand for {remaining} sec",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

        # ================== EMERGENCY CONFIRMED ==================
        if elapsed >= PANIC_TIME and not emergency_confirmed:
            emergency_confirmed = True
            print(">>> EMERGENCY CONFIRMED <<<")

        if emergency_confirmed:
            cv2.putText(
                frame,
                "EMERGENCY DETECTED!",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

            if not screenshot_taken:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{SCREENSHOT_DIR}/emergency_{timestamp}.jpg"
                cv2.imwrite(filename, frame)

                print("[INFO] Screenshot saved:", filename)
                send_email_alert(filename)

                screenshot_taken = True

    # ================== NO HAND → RESET ==================
    else:
        panic_start_time = None
        emergency_confirmed = False
        screenshot_taken = False

    cv2.imshow("AI Emergency Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ================== CLEANUP ==================
cap.release()
cv2.destroyAllWindows()

