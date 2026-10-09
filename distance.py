import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")

# Camera focal length from calibration
FOCAL_LENGTH = 1050

# Real width of our bottle
KNOWN_WIDTH = 8  # cm

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened")
    exit()

print("Camera started!")
print("Press Q to quit.")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read camera frame")
        break

    # Detect objects
    results = model(frame, verbose=False)

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # We are measuring the bottle
            if class_name == "bottle":

                # Get bounding box
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                # Calculate width in pixels
                width_pixels = x2 - x1

                if width_pixels > 0:

                    # Distance formula
                    distance = (
                        KNOWN_WIDTH * FOCAL_LENGTH
                    ) / width_pixels

                    # Draw bounding box
                    cv2.rectangle(
                        frame,
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        (0, 255, 0),
                        2
                    )

                    # Display distance
                    text = f"Bottle: {distance:.1f} cm"

                    cv2.putText(
                        frame,
                        text,
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

    # Display camera
    cv2.imshow("Object Distance", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()