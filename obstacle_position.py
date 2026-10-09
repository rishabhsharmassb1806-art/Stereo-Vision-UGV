import cv2
from ultralytics import YOLO

# --------------------------------
# SETTINGS
# --------------------------------

FOCAL_LENGTH = 1050
KNOWN_WIDTH = 8          # cm
STOP_DISTANCE = 100      # cm
CONFIDENCE = 0.5

# Load YOLO model
model = YOLO("yolo11n.pt")

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera could not be opened")
    exit()

print("✅ Obstacle position detection started")
print("Press Q to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("❌ Could not read camera")
        break

    # Get frame dimensions
    height, width = frame.shape[:2]

    # Divide camera into 3 zones
    left_boundary = width // 3
    right_boundary = (width * 2) // 3

    # Draw zone lines
    cv2.line(
        frame,
        (left_boundary, 0),
        (left_boundary, height),
        (255, 255, 255),
        2
    )

    cv2.line(
        frame,
        (right_boundary, 0),
        (right_boundary, height),
        (255, 255, 255),
        2
    )

    # Zone labels
    cv2.putText(
        frame,
        "LEFT",
        (30, height - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "CENTER",
        (width // 2 - 50, height - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "RIGHT",
        (width - 100, height - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # --------------------------------
    # YOLO DETECTION
    # --------------------------------

    results = model(frame, verbose=False)

    closest_distance = float("inf")
    closest_position = None
    closest_object = None

    for result in results:

        for box in result.boxes:

            confidence = float(box.conf[0])

            if confidence < CONFIDENCE:
                continue

            # Object class
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # Bounding-box center
            center_x = (x1 + x2) // 2

            # Width in pixels
            object_width = x2 - x1

            if object_width <= 0:
                continue

            # --------------------------------
            # DISTANCE
            # --------------------------------

            distance = (
                KNOWN_WIDTH * FOCAL_LENGTH
            ) / object_width

            # --------------------------------
            # POSITION
            # --------------------------------

            if center_x < left_boundary:

                position = "LEFT"

            elif center_x < right_boundary:

                position = "CENTER"

            else:

                position = "RIGHT"

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Object information
            text = f"{class_name} {distance:.1f}cm {position}"

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
            # FIND CLOSEST OBJECT
            # --------------------------------

            if distance < closest_distance:

                closest_distance = distance
                closest_position = position
                closest_object = class_name

    # --------------------------------
    # SAFETY DECISION
    # --------------------------------

    if closest_distance < STOP_DISTANCE:

        warning = (
            f"STOP! {closest_object} "
            f"{closest_distance:.1f} cm "
            f"({closest_position})"
        )

        cv2.putText(
            frame,
            warning,
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            3
        )

    else:

        cv2.putText(
            frame,
            "ROAD CLEAR",
            (30, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            3
        )

    # Show result
    cv2.imshow(
        "UGV Obstacle Position",
        frame
    )

    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------
# CLEANUP
# --------------------------------

cap.release()
cv2.destroyAllWindows()