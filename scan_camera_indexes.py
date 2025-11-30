import cv2

print("Scanning available camera indices...")
for i in range(10):
    cap = cv2.VideoCapture(i, cv2.CAP_AVFOUNDATION)
    if cap.isOpened():
        print(f"Camera index {i} is available")
        cap.release()