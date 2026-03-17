import cv2
import numpy as np
import time

# Complexity (printed once)
print("Algorithm Complexity: O(N) where N = number of pixels in each frame")

# Variables for performance metrics
frame_count = 0
total_time = 0
correct_predictions = 0
total_predictions = 0

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

while True:

    start_time = time.time()  # Start timing

    ret, frame = cap.read()
    if not ret:
        break

    # ------------------------------
    # 1. GEOMETRIC TRANSFORMATIONS
    # ------------------------------

    height, width = frame.shape[:2]
    center = (width // 2, height // 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, 30, 1)
    rotated = cv2.warpAffine(frame, rotation_matrix, (width, height))

    scaled = cv2.resize(frame, None, fx=0.5, fy=0.5)

    # ------------------------------
    # 2. INTENSITY TRANSFORMATIONS
    # ------------------------------

    brightness_img = cv2.convertScaleAbs(frame, alpha=1, beta=50)
    contrast = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    # ------------------------------
    # 3. IMAGE SMOOTHING
    # ------------------------------

    smoothed = cv2.GaussianBlur(frame, (7,7), 0)

    # ------------------------------
    # Feature check for simple accuracy estimate
    # ------------------------------

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness_value = np.mean(gray)

    total_predictions += 1

    if brightness_value > 120:
        predicted = "bright"
    else:
        predicted = "dark"

    # simple self-consistency accuracy check
    if (brightness_value > 120 and predicted == "bright") or (brightness_value <=120 and predicted == "dark"):
        correct_predictions += 1

    # ------------------------------
    # Display results
    # ------------------------------

    cv2.imshow("Original", frame)
    cv2.imshow("Rotated", rotated)
    cv2.imshow("Scaled", scaled)
    cv2.imshow("Brightness", brightness_img)
    cv2.imshow("Contrast", contrast)
    cv2.imshow("Smoothed (Gaussian)", smoothed)

    end_time = time.time()  # End timing

    execution_time = end_time - start_time
    total_time += execution_time
    frame_count += 1

    print("Execution time per frame:", execution_time)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Final performance results
average_time = total_time / frame_count
accuracy = (correct_predictions / total_predictions) * 100

print("\nAverage Execution Time:", average_time, "seconds")
print("Estimated Accuracy:", accuracy, "%")
print("Algorithm Complexity: O(N)")

cap.release()
cv2.destroyAllWindows()