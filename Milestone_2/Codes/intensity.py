import cv2
import numpy as np
import serial
import time

print("Algorithm Complexity: O(N) where N = number of pixels per frame")

arduino = serial.Serial('COM6', 9600)
time.sleep(2)

cap = cv2.VideoCapture(0)

last_command = None

frame_count = 0
total_time = 0
correct_predictions = 0
total_predictions = 0

while True:

    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    # --------------------------
    # Geometric Transformations
    # --------------------------

    height, width = frame.shape[:2]
    center = (width//2, height//2)

    rot_matrix = cv2.getRotationMatrix2D(center, 30, 1)
    rotated = cv2.warpAffine(frame, rot_matrix, (width, height))

    scaled = cv2.resize(frame, None, fx=0.5, fy=0.5)

    # --------------------------
    # Intensity Transformations
    # --------------------------

    bright_img = cv2.convertScaleAbs(frame, alpha=1, beta=40)
    contrast_img = cv2.convertScaleAbs(frame, alpha=1.5, beta=0)

    # --------------------------
    # Smoothing
    # --------------------------

    smooth = cv2.GaussianBlur(frame,(7,7),0)

    # --------------------------
    # Feature Extraction
    # --------------------------

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    brightness = np.mean(gray)

    edges = cv2.Canny(gray,100,200)
    edge_count = np.sum(edges)/255

    total_predictions += 1

    # --------------------------
    # Closed Loop Decision
    # --------------------------

    if brightness > 130:
        command = 'C'
        text = "Bright -> Servo Clockwise"

    elif edge_count > 4000:
        command = 'F'
        text = "Many edges -> Servo Fast"

    else:
        command = 'A'
        text = "Dark -> Servo Counter Clockwise"

    # simple consistency accuracy
    if (brightness > 130 and command == 'C') or (brightness <=130 and command == 'A'):
        correct_predictions += 1

    if command != last_command:
        arduino.write(command.encode())
        last_command = command
        print(text)

    cv2.imshow("Original", frame)
    cv2.imshow("Edges", edges)
    cv2.imshow("Smoothed", smooth)

    end_time = time.time()

    execution_time = end_time - start_time
    total_time += execution_time
    frame_count += 1

    print("Execution time per frame:", execution_time)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

average_time = total_time / frame_count
accuracy = (correct_predictions / total_predictions) * 100

print("\nAverage Execution Time:", average_time, "seconds")
print("Estimated Accuracy:", accuracy, "%")
print("Algorithm Complexity: O(N)")

cap.release()
arduino.close()
cv2.destroyAllWindows()