# Note: code works on macOS M1
import cv2
import mediapipe as mp

# ------------------------------
# MediaPipe setup
# ------------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Finger tip indices in MediaPipe
FINGER_TIPS = [4, 8, 12, 16, 20]
THUMB_MCP = 2
WRIST = 0

# ------------------------------
# Camera setup (macOS M1/M2)
# ------------------------------
cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)  # Use camera index 1

if not cap.isOpened():
    print("ERROR: Camera failed to open!")
    exit()

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from camera.")
            break

        # Flip horizontally for mirror view
        frame = cv2.flip(frame, 1)

        # Convert BGR to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        finger_count = 0

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = [lm for lm in hand_landmarks.landmark]

            # Detect if hand is right or left
            is_right_hand = landmarks[WRIST].x < landmarks[THUMB_MCP].x

            # Thumb
            if (is_right_hand and landmarks[FINGER_TIPS[0]].x > landmarks[THUMB_MCP].x) or \
               (not is_right_hand and landmarks[FINGER_TIPS[0]].x < landmarks[THUMB_MCP].x):
                finger_count += 1

            # Other fingers (index, middle, ring, pinky)
            for tip in FINGER_TIPS[1:]:
                if landmarks[tip].y < landmarks[tip - 2].y:
                    finger_count += 1

            # Display finger count
            cv2.putText(frame, f"Fingers: {finger_count}", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 255, 0), 4)

        cv2.imshow("Finger Counter", frame)

        # Press ESC to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()