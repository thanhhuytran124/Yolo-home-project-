import os
import cv2 as cv
import numpy as np

#replace the list with the person image folder name
people = ['Ben Afflek', 'Chris Evan', 'Christian Bale']

haar_cascade = cv.CascadeClassifier('haar_face.xml')
features = []
labels = []

def get_faces_and_labels(faces_folder_path):
    """
    faces_folder_path -> the path to the image_file
    return 2 variables, features list and labels list
    """
    features = []
    labels = []
    for person in people:
        img_folder_path = os.path.join(faces_folder_path, person)
        label = people.index(person)
        for img in os.listdir(img_folder_path):
            img_path = os.path.join(img_folder_path, img)
            img_matrix = cv.imread(img_path)
            if img_matrix is None: 
                continue
            gray_img = cv.cvtColor(img_matrix, cv.COLOR_BGR2GRAY)
            gray_img = cv.GaussianBlur(gray_img, (3, 3), 0)
            gray_img = cv.equalizeHist(gray_img)
            seq_faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, minNeighbors=4)
            for x, y, width, height in seq_faces_rect:
                face_region = gray_img[y : y + height, x : x + width]
                features.append(face_region)
                labels.append(label)
    return features, labels    

print("Preparing images to train...")
features, labels = get_faces_and_labels(r"Faces\train")
features = np.array(features, dtype= 'object')
labels = np.array(labels)

face_recognizer = cv.face.LBPHFaceRecognizer.create(radius=1, neighbors=8, grid_x=4, grid_y=4)
print("Training model...")
face_recognizer.train(features, labels)
face_recognizer.write('face_recognizer_model.yml')
print("Training model success!")