# Importing Libraries
import cv2
import os
import numpy as np
from PIL import Image

# Initializing paths
train_folder =  'D:/final year project/backend/New folder/'
test_folder = 'd:/final year project/backend/temp.jpg'
face_cascade = cv2.CascadeClassifier('d:/final year project/backend/xml/haarcascade_frontalface_alt2.xml')

cam = cv2.VideoCapture(0) # Creating camera object

# Function to generate image database
def get_data(file_path):
    faces = []
    uids = []
    for file in os.listdir(train_folder):
        path = train_folder + file
        uid = int(file.strip('.jpg')) # Generate unique id
        img = Image.open(path).convert('L') # Making channel singular
        img_np = np.array(img, 'uint8') # Convert to numpy array
        faces.append(img_np)
        uids.append(uid)
    return faces, uids

# Capture live image for recognition
while True: 
    ret, frame = cam.read()
    if not ret: # if statement used to escape errors
        break
    else:
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
        face = face_cascade.detectMultiScale(frame, 1.1, 4) # Detect face
        cv2.imshow("window", frame)

        k = cv2.waitKey(1)
        if k == ord('q'): # ord() gives unicode of the letter
            print("Exited successfully!")
            break
        # Crop face
        elif k == ord(' '):
            for (x, y, w, h) in face:
                face = frame[y:y + h, x:x + w] 
            face = cv2.equalizeHist(face)
            face = cv2.resize(face, (640, 640)) # Increasiing resolution
            cv2.imwrite(test_folder, face)

            faces, uids = get_data(train_folder)
            model = cv2.face.LBPHFaceRecognizer_create() # Model for LBPH
            model.train(faces, np.array(uids))
            test_img = Image.open(test_folder).convert('L')
            test_np = np.array(test_img, 'uint8')
            prediction = model.predict(test_np)
            print(prediction[0]) # Printing result ignoring confidence score which is [1]
            cam.release()
            cv2.destroyAllWindows()
cam.release()
cv2.destroyAllWindows()



