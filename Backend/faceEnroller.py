# Import libraries
import cv2

# Assigning paths
file_path = 'D:/final year project/backend/New folder/'
face_cascade = cv2.CascadeClassifier('d:/final year project/backend/xml/haarcascade_frontalface_alt2.xml')

cam = cv2.VideoCapture(0) # Creating camera object

# Storing captured photos
while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    face = face_cascade.detectMultiScale(frame, 1.1, 4) # Detect face
    cv2.imshow("window", frame)

    k = cv2.waitKey(1)
    if k == ord('q'): # ord() gives unicode of letter
        print("Exited successfully!")
        break
    elif k == ord(' '):
        username = input("Enter student's moodle ID: ")
        # Crop face
        for (x, y, w, h) in face:
            face = frame[y:y + h, x:x + w] 
        face = cv2.equalizeHist(face) # Equalize histogram for improving accuracy
        face = cv2.resize(face, (640, 640))
        cv2.imwrite(file_path + username + '.jpg', face)
        print('Image saved successfully!')
cam.release()
cv2.destroyAllWindows()