import tkinter as tk
from tkinter import StringVar, OptionMenu
from datetime import datetime

#root is the instance of the tk class 
#creats the basic gui
# Create a function to get and display the current date
def get_current_date(date_entry_widget):
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_entry_widget.delete(0, tk.END)  # Clear any existing text
    date_entry_widget.insert(0, current_date)

def start_attendance():
    # Implement the logic to submit attendance here

    print(f"Attendance Started ")

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
    back_button.pack( padx=10, pady=10 , side=tk.LEFT , anchor = "nw")

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
    take_atten.minsize(200, 100)
    take_atten.maxsize(1200, 988)
    
    take_atten.mainloop()

attendence_root = tk.Tk()

# width x height
attendence_root.geometry("644x434")

# Set the dimensions of the main window
attendence_root.geometry("644x434")

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
b2 = tk.Button(center_frame, text="Enroll",font=('Bold', 12), bg='#1877f2', fg='white', width=8, borderwidth=3, relief=tk.SUNKEN)
b2.pack(pady=10)

# Center the frame within the window
center_frame.place(in_=attendence_root, anchor="c", relx=0.5, rely=0.5)

# Set the dimensions of the main window
attendence_root.minsize(200, 100)
attendence_root.maxsize(1200, 988)

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