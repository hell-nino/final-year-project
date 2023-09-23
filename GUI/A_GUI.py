import tkinter as tk
from tkinter import StringVar, OptionMenu
from datetime import datetime
import cv2
import os
import numpy as np
from PIL import Image

#root is the instance of the tk class 
#creats the basic gui
# Create a function to get and display the current date
def get_current_date(date_entry_widget):
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_entry_widget.delete(0, tk.END)  # Clear any existing text
    date_entry_widget.insert(0, current_date)


def start_attendance():
    # Implement the logic to submit attendance here
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


def take_attendence():
    take_atten = tk.Tk()
    timeFrom = ["9:10 AM - 10:30 AM","11:00 AM - 11:55 AM ", "11:55 AM - 12:50 PM","1:20 PM - 2:15 PM","2:15 PM - 3:10 PM"]
    variableTime = StringVar(take_atten)
    variableTime.set("Time")
    dropTime = OptionMenu(take_atten, variableTime, *timeFrom)
    dropTime.pack()

    Sub = ["Microwave Engineering", "Mobile Communication", "Internet communication System", "Cloud computing and security", "Management information system"]
    variableSub = StringVar(take_atten)
    variableSub.set("Subject")
    dropSub = OptionMenu(take_atten, variableSub, *Sub)
    dropSub.pack()

    # Create a Back button
    back_button = tk.Button(take_atten, text="Back",font=('Bold', 12), bg='#1877f2', fg='white', width=15, command=take_atten.destroy)
    back_button.pack( padx=10, pady=10 , side=tk.BOTTOM , anchor = "nw")

    # Entry widget to display the current date
    date_entry = tk.Entry(take_atten, font=("Helvetica", 16))
    date_entry.pack(pady=20)

    # Create a button to update the current date
    update_button = tk.Button(take_atten, text="Get Current Date",font=('Bold', 12), bg='#1877f2', fg='white', width=15, command=lambda: get_current_date(date_entry))
    update_button.pack()
    
    # Create a Start button

    start_button = tk.Button(take_atten, text="Start",font=('Bold', 12), bg='#1877f2', fg='white', width=12, command=start_attendance)
    start_button.pack(pady=10)

    # Set the dimensions of the window
    take_atten.minsize(480, 800)
    take_atten.maxsize(480, 800)
    
    take_atten.mainloop()


def get_id():
        # Function to validate and get the entered username
    def start_Enrolling():
        username = username_entry.get()
        username.isdigit()
        print("Username:", username)


    # Function to enable/disable the submit button based on input
    def check_input():
        if username_entry.get().isdigit():
            submit_button.config(state="normal")
        else:
            submit_button.config(state="disabled")

    # Create the main window
    root = tk.Tk()
    root.title("Integer Username Input Box")

    # Calculate the center coordinates
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Create a frame to hold the input and submit widgets
    frame = tk.Frame(root)
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create a Label widget for instructions
    label = tk.Label(frame, text="Enter MoodleId :",font=('Bold', 12), relief=tk.SUNKEN)
    label.grid(row=0, column=0, padx=10, pady=10)

    # Create an Entry widget for the username
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1, padx=10, pady=10)
    username_entry.bind("<KeyRelease>", lambda event: check_input())  # Check input on key release

    # Create a Button widget to submit the username
    submit_button = tk.Button(frame, text="Submit", command=start_Enrolling, state="disabled",font=('Bold', 12), bg='#1877f2', fg='white', width=8, borderwidth=3, relief=tk.SUNKEN)
    submit_button.grid(row=1, columnspan=2, padx=10, pady=10)

    root.minsize(480, 800)
    root.maxsize(480, 900)
    # Start the Tkinter main loop
    root.mainloop()


attendence_root = tk.Tk()

# width x height
attendence_root.geometry("480x800")

# Set the dimensions of the main window
#attendence_root.geometry("644x434")

# Create a frame for centering
center_frame = tk.Frame(attendence_root)
center_frame.pack(expand=True, fill="both")

f1 = tk.Frame(attendence_root, bg="grey", borderwidth=6, relief=tk.SUNKEN)
f1.pack(side=tk.TOP, fill="x")

l = tk.Label(f1, text="Attendance System", font=("comicsense", 19, "bold"))
l.pack()

# Create a button for taking attendance
b1 = tk.Button(center_frame, text="Take Attendance",font=('Bold', 12), bg='#1877f2', fg='white', width=15, borderwidth=3, relief=tk.SUNKEN, command=take_attendence)
b1.pack(pady=10)  # Add some vertical padding between the buttons

# Create a button for enrolling
b2 = tk.Button(center_frame, text="Enroll",font=('Bold', 12), bg='#1877f2', fg='white', width=8, borderwidth=3, relief=tk.SUNKEN,command=get_id)
b2.pack(pady=10)

# Center the frame within the window
center_frame.place(in_=attendence_root, anchor="c", relx=0.5, rely=0.5)

# Set the dimensions of the main window
attendence_root.minsize(480, 800)
attendence_root.maxsize(480, 900)

#impportant label options
# text --> adds_the_text
# bg  -- > background
# fg -- > foreround
# font  -- >sets the Fontsss
# padx --> x padding
# pady -- > y padding
# rerelief --> border styling --- SUNKEN RAISED GROOVE RIDGE

# title of the project  
# title = Label(text="Attendence System",bg="red",fg="white",padx=20,pady=20 , font=("comicsense" , 19 , "bold"), borderwidth=3 , relief=SUNKEN)

#important pack attribute
# anchor = nw , ne 
#side = top , bottom , left , right
#fill 
#padx 
#pady

#title.pack(side=LEFT , anchor = "nw", fill=X )


#event loop
attendence_root.mainloop()