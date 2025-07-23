import cv2
import os
import numpy as np
import pickle
import time

class FaceRecognizer:
    """
    A class to handle all face recognition tasks, including training the model
    and recognizing faces from a live camera feed.
    """
    def __init__(self, dataset_path='known_faces', trainer_path='trainer'):
        """
        Initializes the FaceRecognizer with paths and loads the face detector.
        
        Args:
            dataset_path (str): Path to the directory containing subdirectories of face images.
            trainer_path (str): Path to the directory where the trained model will be saved.
        """
        self.dataset_path = dataset_path
        self.trainer_path = trainer_path
        self.model_path = os.path.join(self.trainer_path, 'trained_model.yml')
        self.labels_path = os.path.join(self.trainer_path, 'labels.pkl')
        
        # Use the LBPH (Local Binary Patterns Histograms) recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        # Load the pre-built Haar cascade for frontal face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        self.labels = {}

    def train(self):
        """
        Trains the face recognizer model on the images in the dataset directory.
        The dataset directory should contain one subdirectory for each person,
        named with the person's name.
        """
        if not os.path.exists(self.dataset_path):
            print(f"[ERROR] Dataset directory not found at '{self.dataset_path}'")
            return False

        print("[INFO] Starting model training...")
        faces = []
        ids = []
        label_ids = {}
        current_id = 0

        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                if file.endswith(("png", "jpg", "jpeg")):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()

                    if label not in label_ids:
                        label_ids[label] = current_id
                        current_id += 1
                    
                    id_ = label_ids[label]
                    
                    # Load the image and convert to grayscale
                    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    if image is None:
                        continue
                    
                    # Detect faces in the image
                    detected_faces = self.face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
                    for (x, y, w, h) in detected_faces:
                        roi = image[y:y+h, x:x+w]
                        faces.append(roi)
                        ids.append(id_)

        if not faces:
            print("[ERROR] No faces found in the dataset to train. Please populate the 'known_faces' directory.")
            return False

        # Save the label dictionary (id -> name)
        os.makedirs(self.trainer_path, exist_ok=True)
        with open(self.labels_path, 'wb') as f:
            pickle.dump({v: k for k, v in label_ids.items()}, f)

        # Train the recognizer and save the model
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.save(self.model_path)
        print(f"[INFO] Training complete. {len(np.unique(ids))} faces trained.")
        return True

    def load_trained_model(self):
        """Loads the trained model and labels from disk."""
        if not os.path.exists(self.model_path) or not os.path.exists(self.labels_path):
            print("[WARNING] Trained model not found. Please run the training first.")
            return False
        
        self.recognizer.read(self.model_path)
        with open(self.labels_path, 'rb') as f:
            # Load the labels: {0: 'person_a', 1: 'person_b', ...}
            self.labels = pickle.load(f)
        print("[INFO] Trained model and labels loaded successfully.")
        return True

    def recognize_face(self, cam_index=0, timeout=10, required_recognitions=5, confidence_threshold=75):
        """
        Recognizes a face from the camera feed. Requires multiple confident
        matches before returning a name.

        Args:
            cam_index (int): The index of the camera to use.
            timeout (int): How many seconds to search for a face.
            required_recognitions (int): How many consecutive matches are needed.
            confidence_threshold (int): A value from 0-100. Lower is more confident.

        Returns:
            str: The name of the recognized person, or None if not recognized.
        """
        if not self.labels:
            print("[ERROR] No labels loaded. Cannot recognize faces.")
            return None

        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            print(f"[ERROR] Cannot open camera at index {cam_index}")
            return None

        print("[INFO] Looking for a known face...")
        start_time = time.time()
        last_recognized_id = -1
        recognition_count = 0

        while time.time() - start_time < timeout:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                id_, confidence = self.recognizer.predict(roi_gray)

                # A confidence of 0 is a perfect match.
                if confidence < confidence_threshold:
                    name = self.labels.get(id_, "Unknown")
                    print(f"[DEBUG] Potential match: {name} with confidence {confidence:.2f}")

                    if id_ == last_recognized_id:
                        recognition_count += 1
                    else:
                        last_recognized_id = id_
                        recognition_count = 1 # Reset count for new person
                    
                    if recognition_count >= required_recognitions:
                        print(f"[SUCCESS] Confidently recognized: {name}")
                        cap.release()
                        cv2.destroyAllWindows()
                        return name
                else:
                    # If confidence is too low, reset the counter
                    recognition_count = 0
                    last_recognized_id = -1

            # Optional: Display the camera feed for debugging
            # cv2.imshow('Face Recognition', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] No face was confidently recognized within the time limit.")
        return None

