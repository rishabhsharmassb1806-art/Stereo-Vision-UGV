import cv2
from ultralytics import YOLO

# Load YOLO
model = YOLO("yolo11n.pt")

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened")
    exit()

print("Put the 8 cm bottle exactly 30 cm from the camera.")
print("Press Q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, verbose=False)

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # We only want a bottle
            if class_name == "bottle":
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                width_pixels = x2 - x1

                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Bottle width: {width_pixels:.1f} px",
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

    cv2.imshow("Bottle Calibration", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()