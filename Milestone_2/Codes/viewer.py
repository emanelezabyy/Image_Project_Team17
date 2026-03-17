import cv2
import time
import os

while True:
    images = {
        "Original": "original.jpg",
        "Rotated": "rotated.jpg",
        "Scaled": "scaled.jpg",
        "Brightness": "brightness.jpg",
        "Contrast": "contrast.jpg",
        "Smoothed": "smoothed.jpg"
    }

    for name, file in images.items():
        if os.path.exists(file):
            img = cv2.imread(file)
            if img is not None:
                cv2.imshow(name, img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.05)

cv2.destroyAllWindows()
