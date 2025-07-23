import cv2
import os

# Parameters
person_name = "Ayush1"  # 👈 Change this to your name
save_dir = f"known_faces/{person_name}"
os.makedirs(save_dir, exist_ok=True)

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
count = 0
print("[INFO] Starting face capture. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{save_dir}/{count}.jpg", face)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Capturing Faces", frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
        break

cap.release()
cv2.destroyAllWindows()
print(f"[INFO] Saved {count} images to {save_dir}")
