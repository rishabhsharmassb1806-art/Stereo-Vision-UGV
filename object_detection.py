import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open laptop camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera could not be opened")
    exit()

print("✅ Camera started")
print("Press Q to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Could not read frame")
        break

    # Detect objects
    results = model(frame, verbose=False)

    # Draw detected objects
    annotated_frame = results[0].plot()

    # Show result
    cv2.imshow("YOLO Object Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()