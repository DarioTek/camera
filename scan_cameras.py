import cv2

def list_and_test_cameras(max_test=5):
    print("Scanning available cameras on macOS...\n")
    for index in range(max_test):
        print(f"Testing index {index}...")

        cap = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)

        if not cap.isOpened():
            print(f" ❌ Camera {index} could NOT be opened.\n")
            continue

        # Try grabbing one frame
        ret, frame = cap.read()
        if ret:
            print(f" ✅ Camera {index} WORKS and can capture frames.\n")
        else:
            print(f" ⚠️ Camera {index} OPENED but cannot read frames.\n")

        cap.release()

list_and_test_cameras()