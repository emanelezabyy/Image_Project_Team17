import cv2
import numpy as np
import subprocess

print("Algorithm Complexity: O(N) where N = number of pixels in each frame")

# Camera settings
width = 640
height = 480

# Start camera stream
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

while True:
    frame_size = width * height * 3 // 2
    raw = process.stdout.read(frame_size)

    if len(raw) != frame_size:
        break

    yuv = np.frombuffer(raw, dtype=np.uint8).reshape((height * 3 // 2, width))
    frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

    # ------------------------------
    # PROCESSING
    # ------------------------------
    h, w = frame.shape[:2]
    center = (w // 2, h // 2)

    rotated = cv2.warpAffine(frame, cv2.getRotationMatrix2D(center, 30, 1), (w, h))
    scaled = cv2.resize(frame, None, fx=0.5, fy=0.5)

    brightness_img = cv2.convertScaleAbs(frame, alpha=1, beta=50)
    contrast = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    smoothed = cv2.GaussianBlur(frame, (7, 7), 0)

    # ------------------------------
    # SAVE IMAGES
    # ------------------------------
    cv2.imwrite("/home/pi/stream/original.jpg", frame)
    cv2.imwrite("/home/pi/stream/rotated.jpg", rotated)
    cv2.imwrite("/home/pi/stream/scaled.jpg", scaled)
    cv2.imwrite("/home/pi/stream/brightness.jpg", brightness_img)
    cv2.imwrite("/home/pi/stream/contrast.jpg", contrast)
    cv2.imwrite("/home/pi/stream/smoothed.jpg", smoothed)

    frame_count += 1
    print("Frame:", frame_count)

process.terminate()
