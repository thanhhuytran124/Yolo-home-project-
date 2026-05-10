import cv2 as cv

people = ['Ben Afflek', 'Chris Evan', 'Christian Bale']
haar_cascade = cv.CascadeClassifier('haar_face.xml')

#path to the video for face regcognition
Christian_Bale = r"Faces/test/christian_bale/Test_Christian Bale.mp4" 
Ben_Afflek = r"Faces/test/ben_afflek/Ben_Affleck.mp4"
Chris_Evan = r"Faces/test/chris_evan/Chris_Evan.mp4"

face_recognizer = cv.face.LBPHFaceRecognizer.create(radius=1, neighbors=8, grid_x=4, grid_y=4)
face_recognizer.read("face_recognizer_model.yml")

def resize(frame, scale=0.5):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

#insert variable video (Ben_Afflek, Christian_Bale, Chris_Evan) here
vid = cv.VideoCapture(Christian_Bale)

print("Processing video... press d to quit")

while True:
    isTrue, frame = vid.read()
    if not isTrue:
        print("video end or cannot read")
        break

    frame = resize(frame, scale=0.7) 
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    face_regions = haar_cascade.detectMultiScale(gray_frame, 1.1, 6)

    for (x, y, w, h) in face_regions:
        face_region = gray_frame[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face_region)
        
        if confidence < 10:
            name = people[label]
            color = (0, 255, 0) 
        else:
            name = "Unknown"
            color = (0, 0, 255) 

        cv.putText(frame, f"{name} ({int(confidence)})", (x, y - 10), cv.FONT_HERSHEY_COMPLEX, 0.6, color, thickness=2)
        cv.rectangle(frame, (x, y), (x + w, y + h), color, thickness=2)
    cv.imshow('Live face recongition', frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

vid.release()
cv.destroyAllWindows()
