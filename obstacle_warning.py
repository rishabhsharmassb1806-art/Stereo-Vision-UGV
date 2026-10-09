import cv2
from ultralytics import YOLO

# -----------------------------
# SETTINGS
# -----------------------------

FOCAL_LENGTH = 1050
KNOWN_WIDTH = 8       # cm
STOP_DISTANCE = 100   # cm

# Load YOLO
model = YOLO("yolo11n.pt")

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera could not be opened")
    exit()

print("✅ Obstacle detection started")
print("Press Q to quit")

# -----------------------------
# MAIN LOOP
# -----------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("❌ Could not read camera")
        break

    results = model(frame, verbose=False)

    obstacle_found = False

    for result in results:

        for box in result.boxes:

            # Confidence
            confidence = float(box.conf[0])

            # Ignore weak detections
            if confidence < 0.5:
                continue

            # Object name
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # Width in pixels
            width_pixels = x2 - x1

            if width_pixels <= 0:
                continue

            # --------------------------------
            # Distance calculation
            # --------------------------------

            distance = (KNOWN_WIDTH * FOCAL_LENGTH) / width_pixels

            # --------------------------------
            # Check danger distance
            # --------------------------------

            if distance < STOP_DISTANCE:
                obstacle_found = True

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Object + distance
            text = f"{class_name} | {distance:.1f} cm"

            cv2.putText(
                frame,
                text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # --------------------------------
    # WARNING
    # --------------------------------

    if obstacle_found:

        cv2.putText(
            frame,
            "!!! STOP - OBSTACLE !!!",
            (50, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 0, 255),
            3
        )

    else:

        cv2.putText(
            frame,
            "SAFE",
            (50, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

    # Show camera
    cv2.imshow("UGV Obstacle Warning", frame)

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# CLEANUP
# -----------------------------

cap.release()
cv2.destroyAllWindows()