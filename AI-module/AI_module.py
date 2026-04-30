#Dependecies: pip install opencv-python mediapipe numpy
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import os

class FaceRecognizer:
    def __init__(self):
        # Face options
        base_options = python.BaseOptions(model_asset_path='detector.tflite')
        options = vision.FaceDetectorOptions(base_options=base_options)
        self.detector = vision.FaceDetector.create_from_options(options)
        
        #Recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_map = {} # Maps ID numbers to Folder Names

    def train(self, dataset_path):
        """Processes subfolders and trains the recognizer."""
        faces = []
        labels = []
        current_id = 0

        if not os.path.exists(dataset_path):
            print(f"[ERROR] Path {dataset_path} does not exist!")
            return

        print("[INFO] Training AI on your dataset...")
        #Append images and labels for model to learn
        for person_name in os.listdir(dataset_path):
            person_dir = os.path.join(dataset_path, person_name)
            if not os.path.isdir(person_dir): continue

            self.label_map[current_id] = person_name
            for image_name in os.listdir(person_dir):
                img_path = os.path.join(person_dir, image_name)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None: continue
                
                img = cv2.resize(img, (200, 200))
                faces.append(img)
                labels.append(current_id)
            current_id += 1

        # Use the collected data to train the recognizer
        if len(faces) > 0:
            self.recognizer.train(faces, np.array(labels))
            print(f"[INFO] Success! Loaded {len(self.label_map)} people.")
        else:
            print("[ERROR] No images found in dataset folders.")

    def identify_faces(self, frame):
        """Detects and returns names + coordinates."""
        # Convert OpenCV BGR to MediaPipe RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Detect faces
        detection_result = self.detector.detect(mp_image)
        results_list = []

        # If faces are detected, process each one
        if detection_result.detections:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for detection in detection_result.detections:
                bbox = detection.bounding_box
                x, y, w, h = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
                
                # Crop and Recognize
                face_roi = gray[max(0,y):y+h, max(0,x):x+w]
                if face_roi.size == 0: continue
                
                face_roi = cv2.resize(face_roi, (200, 200))
                label_id, confidence = self.recognizer.predict(face_roi)

                
                name = self.label_map.get(label_id, "Unknown") if confidence < 90 else "Unknown"
                
                results_list.append({
                    "name": name,
                    "box": (x, y, w, h),
                    "confidence": round(confidence, 2)
                })
        
        return results_list
    

if __name__ == "__main__":
    #Initialization
    recognizer = FaceRecognizer()
    recognizer.train('face_dataset/')

    #Try the detection on webcam feed
    CAMERA_URL = 0 # Placeholder for actual camera URL
    cap = cv2.VideoCapture(CAMERA_URL)

    while True:
        ret, frame = cap.read()
        if not ret: break

    # Use the modular function
        identities = recognizer.identify_faces(frame)

        for person in identities:
            x, y, w, h = person["box"]
            name = person["name"]
        
        # Draw on screen
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} (Conf: {person['confidence']})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("IoT Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()