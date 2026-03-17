import cv2
import numpy as np
import time
import subprocess

print("Algorithm Complexity: O(N) where N = number of pixels in each frame")

# Camera settings
width = 640
height = 480

# Start camera stream using rpicam
cmd = [
    "rpicam-vid",
    "--timeout", "0",
    "--codec", "yuv420",
    "--width", str(width),
    "--height", str(height),
    "-o", "-"
]

process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

frame_count = 0
total_time = 0
correct_predictions = 0
total_predictions = 0

while True:
    start_time = time.time()

    frame_size = width * height * 3 // 2
    raw = process.stdout.read(frame_size)

    if len(raw) != frame_size:
        break

    yuv = np.frombuffer(raw, dtype=np.uint8).reshape((height * 3 // 2, width))
    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

    # ------------------------------
    # GEOMETRIC TRANSFORMATIONS
    # ------------------------------
    h, w = frame.shape[:2]
    center = (w // 2, h // 2)

    rot_matrix = cv2.getRotationMatrix2D(center, 30, 1)
    rotated = cv2.warpAffine(frame, rot_matrix, (w, h))

    scaled = cv2.resize(frame, None, fx=0.5, fy=0.5)

    # ------------------------------
    # INTENSITY
    # ------------------------------
    brightness_img = cv2.convertScaleAbs(frame, alpha=1, beta=50)
    contrast = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    # ------------------------------
    # SMOOTHING
    # ------------------------------
    smoothed = cv2.GaussianBlur(frame, (7,7), 0)

    # ------------------------------
    # FEATURE CHECK
    # ------------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness_value = np.mean(gray)

    total_predictions += 1

    if brightness_value > 120:
        predicted = "bright"
    else:
        predicted = "dark"

    if (brightness_value > 120 and predicted == "bright") or \
       (brightness_value <= 120 and predicted == "dark"):
        correct_predictions += 1

    end_time = time.time()

    execution_time = end_time - start_time
    total_time += execution_time
    frame_count += 1

    print("Execution time:", execution_time)

# ------------------------------
# FINAL RESULTS
# ------------------------------
average_time = total_time / frame_count if frame_count > 0 else 0
accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0

print("\nAverage Time:", average_time)
print("Accuracy:", accuracy, "%")
print("Complexity: O(N)")

process.terminate()
