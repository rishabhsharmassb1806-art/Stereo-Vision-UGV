# Stereo Vision UGV

**Stereo-Vision-Based Autonomous Navigation for an Unmanned Ground Vehicle (UGV)**

## Overview

Stereo Vision UGV is a computer vision project focused on obstacle detection, distance estimation, and obstacle position analysis for an unmanned ground vehicle.

The project uses Python, OpenCV, and YOLO-based object detection to explore visual perception for navigation in environments where GPS may be unavailable or unreliable.

## Features

- **Camera Testing:** Verify camera availability and capture video frames.
- **Camera Calibration:** Prepare camera calibration for more reliable geometric measurements.
- **Distance Estimation:** Estimate the distance to objects using the implemented vision approach.
- **Object Detection:** Detect objects using the YOLO model.
- **Obstacle Position Detection:** Analyze obstacle positions within the camera view.
- **Obstacle Warning:** Provide warnings when obstacles are detected according to the implemented logic.

*Note: Feature availability and accuracy depend on the current implementation, camera configuration, and calibration.*

## Technology Stack

- Python
- OpenCV
- YOLO object detection
- NumPy
- Ultralytics YOLO (if used by the current implementation)

## Project Structure

```text
Stereo-Vision-UGV/
├── calibrate.py
├── camera_test.py
├── distance.py
├── object_detection.py
├── obstacle_position.py
├── obstacle_warning.py
├── test.py
├── yolo11n.pt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or a compatible version supported by the installed dependencies
- A compatible camera
- A Windows, Linux, or other supported Python environment
- A webcam or supported camera input
- YOLO model weights (`yolo11n.pt`)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rishabhsharmassb1806-art/Stereo-Vision-UGV.git
cd Stereo-Vision-UGV
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install opencv-python numpy ultralytics
```

Additional dependencies may be required depending on the imports used in individual scripts.

## Running the Project

Run the scripts individually from the project directory.

### Camera test

```bash
python camera_test.py
```

### Camera calibration

```bash
python calibrate.py
```

### Object detection

```bash
python object_detection.py
```

### Distance estimation

```bash
python distance.py
```

### Obstacle position detection

```bash
python obstacle_position.py
```

### Obstacle warning

```bash
python obstacle_warning.py
```

Press `Q` to exit scripts that implement keyboard-based camera-window controls.

**Important:** Camera indices, calibration parameters, model paths, and other settings may need to be configured in the individual scripts before execution.

## How It Works

The project explores a visual perception workflow:

1. Capture images or video from a camera.
2. Detect objects in the camera view.
3. Estimate object distance using the implemented method.
4. Determine the approximate position of obstacles in the image.
5. Generate obstacle warnings based on the detection logic.

Stereo-based depth estimation requires appropriate camera calibration and corresponding left/right image processing. Its accuracy depends on the camera setup and implementation.

## Applications

- Unmanned ground vehicles
- Robotics and computer vision
- Obstacle awareness
- Autonomous navigation research
- GPS-denied environment research

## Future Improvements

- Integrate synchronized stereo cameras.
- Improve depth estimation using stereo disparity.
- Add traversable-ground detection.
- Implement local path planning and obstacle avoidance.
- Integrate real-time motor control with a UGV platform.
- Evaluate detection and distance-estimation accuracy under different lighting conditions.

## Contributing

Contributions, suggestions, and improvements are welcome. Please test changes before submitting them.

## License

A license has not yet been specified. Add an appropriate open-source license before permitting reuse under defined terms.

---

**Project:** Stereo Vision UGV  
**Repository:** https://github.com/rishabhsharmassb1806-art/Stereo-Vision-UGV