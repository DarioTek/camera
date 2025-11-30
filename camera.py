import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

FINGER_TIPS = [4, 8, 12, 16, 20]
WRIST = 0

# ✅ USE CAMERA INDEX 1 on macOS
cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("ERROR: Camera 1 failed to open!")
    exit()

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from camera index 1.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        finger_count = 0

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = [lm for lm in hand_landmarks.landmark]

            # Thumb logic
            if landmarks[FINGER_TIPS[0]].x < landmarks[WRIST].x:
                finger_count += 1

            # Other fingers
            for tip in FINGER_TIPS[1:]:
                if landmarks[tip].y < landmarks[tip - 2].y:
                    finger_count += 1

            cv2.putText(frame, f"Fingers: {finger_count}", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 0), 4)

        cv2.imshow("Finger Counter", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

cap.release()
cv2.destroyAllWindows()