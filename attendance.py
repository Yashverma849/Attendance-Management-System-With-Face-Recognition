import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

# Text-to-speech function
def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# Path configurations
haarcasecade_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/haarcascade_frontalface_default.xml"
trainimagelabel_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/TrainingImageLabel/Trainner.yml"
trainimage_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/StudentDetails/studentdetails.csv"
attendance_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/Attendance"

# Main window with modern design
window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
window.configure(background="#f0f2f5")  # Light gray background

# Add background image
try:
    bg_image = Image.open("attendance.webp")  # Replace with the correct path if needed
    bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = Label(window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Background image not found:", e)
    
# Custom fonts
title_font = font.Font(family="Helvetica", size=28, weight="bold")
button_font = font.Font(family="Arial", size=12, weight="bold")
label_font = font.Font(family="Arial", size=12)

## Center the header and the image in the header
header_frame = Frame(window, bg="#2c3e50", height=80)
header_frame.pack(fill=X)

# Logo and title
try:
    logo = Image.open("UI_Image/BPIT.jpg")  # Updated path
    logo = logo.resize((60, 60), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
    logo_label = Label(header_frame, image=logo1, bg="#2c3e50")
    logo_label.image = logo1
    logo_label.pack(side=LEFT, padx=10, pady=10)  # Keep only the left logo
except Exception as e:
    print("Error loading 'BPIT.jpg':", e)
    logo_label = Label(header_frame, text="LOGO", bg="#2c3e50", fg="white", font=title_font)
    logo_label.pack(side=LEFT, padx=10, pady=10)

# Title
title_label = Label(
    header_frame,
    text="BPIT Attendance System",
    bg="#2c3e50",
    fg="white",
    font=title_font
)
title_label.pack(side=LEFT, padx=10, pady=10)  # Ensure the title is next to the logo

# Welcome label
welcome_label = Label(
    window,
    text="Welcome to BPIT Attendance System",
    bg="#f0f2f5",
    fg="#2c3e50",
    font=("Helvetica", 24, "bold")
)
welcome_label.pack(pady=30)

# Main content frame
content_frame = Frame(window, bg="#f0f2f5")
content_frame.pack(expand=True, fill=BOTH)

# Corrected paths for images
try:
    register_img = Image.open("UI_Image/User.png")  # Updated path
    register_img = register_img.resize((100, 100), Image.LANCZOS)
    register_photo = ImageTk.PhotoImage(register_img)
except Exception as e:
    print("Error loading 'User.png':", e)
    register_photo = None  # Fallback to None if the image is not found

try:
    take_attendance_img = Image.open("UI_Image/take.jpg")  # Updated path
    take_attendance_img = take_attendance_img.resize((100, 100), Image.LANCZOS)
    take_attendance_photo = ImageTk.PhotoImage(take_attendance_img)
except Exception as e:
    print("Error loading 'take.jpg':", e)
    take_attendance_photo = None  # Fallback to None if the image is not found

try:
    view_attendance_img = Image.open("UI_Image/view.webp")  # Updated path
    view_attendance_img = view_attendance_img.resize((100, 100), Image.LANCZOS)
    view_attendance_photo = ImageTk.PhotoImage(view_attendance_img)
except Exception as e:
    print("Error loading 'view.webp':", e)
    view_attendance_photo = None  # Fallback to None if the image is not found

# Corrected path for the logo in the header
try:
    logo = Image.open("UI_Image/BPIT.jpg")  # Updated path
    logo = logo.resize((60, 60), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)
    logo_label = Label(header_frame, image=logo1, bg="#2c3e50")
    logo_label.image = logo1
    logo_label.pack(side=LEFT, padx=20)
except Exception as e:
    print("Error loading 'BPIT.jpg':", e)
    logo_label = Label(header_frame, text="LOGO", bg="#2c3e50", fg="white", font=title_font)
    logo_label.pack(side=LEFT, padx=20)

# Corrected path for the logo in the TakeImageUI
try:
    logo = Image.open("UI_Image/logo.png")  # Updated path
    logo = logo.resize((60, 60), Image.ANTIALIAS)
    logo_img = ImageTk.PhotoImage(logo)
    logo_label = Label(ImageUI, image=logo_img, bg="#2c3e50")
    logo_label.image = logo_img
    logo_label.place(x=10, y=10)
except Exception as e:
    print("Error loading 'logo.png':", e)

# Add images above buttons
if register_photo:
    register_img_label = Label(content_frame, image=register_photo, bg="#f0f2f5")
    register_img_label.place(x=100, y=100)  # Adjust position as needed

if take_attendance_photo:
    take_attendance_img_label = Label(content_frame, image=take_attendance_photo, bg="#f0f2f5")
    take_attendance_img_label.place(x=500, y=100)  # Adjust position as needed

if view_attendance_photo:
    view_attendance_img_label = Label(content_frame, image=view_attendance_photo, bg="#f0f2f5")
    view_attendance_img_label.place(x=900, y=100)  # Adjust position as needed

# Function to create modern buttons
def create_modern_button(parent, text, command, x, y, bg_color="#3498db", hover_color="#2980b9"):
    btn = Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg="white",
        activebackground=hover_color,
        font=button_font,
        bd=0,
        height=2,
        width=25,
        relief=FLAT,
        cursor="hand2"
    )
    
    # Add hover effects
    def on_enter(e):
        btn['background'] = hover_color
    
    def on_leave(e):
        btn['background'] = bg_color
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    btn.place(x=x, y=y)
    return btn

# Create feature buttons with improved UI
register_btn = create_modern_button(
    content_frame, 
    "Register New Student", 
    lambda: TakeImageUI(), 
    100, 220,  # Adjust y-coordinate to place below the image
    bg_color="#3498db"
)

attendance_btn = create_modern_button(
    content_frame, 
    "Take Attendance", 
    lambda: automaticAttedance.subjectChoose(text_to_speech), 
    500, 220,  # Adjust y-coordinate to place below the image
    bg_color="#2ecc71"
)

view_btn = create_modern_button(
    content_frame, 
    "View Attendance", 
    lambda: show_attendance.subjectchoose(text_to_speech), 
    900, 220,  # Adjust y-coordinate to place below the image
    bg_color="#9b59b6"
)

# Footer frame
footer_frame = Frame(window, bg="#2c3e50", height=60)
footer_frame.pack(side=BOTTOM, fill=X)

# Exit button in footer with improved UI
exit_btn = Button(
    footer_frame,
    text="EXIT SYSTEM",
    command=window.quit,
    bg="#e74c3c",
    fg="white",
    activebackground="#c0392b",
    font=button_font,
    bd=0,
    height=1,
    width=15,
    relief=FLAT,
    cursor="hand2"
)

# Add hover effects to exit button
def on_enter_exit(e):
    exit_btn['background'] = "#c0392b"

def on_leave_exit(e):
    exit_btn['background'] = "#e74c3c"

exit_btn.bind("<Enter>", on_enter_exit)
exit_btn.bind("<Leave>", on_leave_exit)
exit_btn.pack(pady=10)

# Error message window
def del_sc1():
    if 'sc1' in globals() and sc1.winfo_exists():
        sc1.destroy()

def err_screen():
    global sc1
    sc1 = tk.Toplevel()
    sc1.geometry("400x150")
    sc1.title("Warning!")
    sc1.configure(background="#f0f2f5")
    sc1.resizable(0, 0)
    
    Label(
        sc1,
        text="Enrollment & Name required!",
        fg="#e74c3c",
        bg="#f0f2f5",
        font=("Arial", 14, "bold"),
    ).pack(pady=20)
    
    Button(
        sc1,
        text="OK",
        command=del_sc1,
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        font=button_font,
        bd=0,
        width=10
    ).pack()

# Validation function
def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Take Image UI with modern design
def TakeImageUI():
    ImageUI = Toplevel()
    ImageUI.title("Register New Student")
    ImageUI.geometry("700x400")
    ImageUI.configure(background="#2c3e50")
    ImageUI.resizable(0, 0)

    # Add logo
    try:
        logo = Image.open("UI_Image/logo.png")
        logo = logo.resize((60, 60), Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = Label(ImageUI, image=logo_img, bg="#2c3e50")
        logo_label.image = logo_img
        logo_label.place(x=10, y=10)
    except Exception as e:
        print("Logo not found:", e)

    # Title
    title = Label(
        ImageUI,
        text="Attendance Management System",
        bg="#2c3e50",
        fg="#1abc9c",
        font=("Helvetica", 24, "bold"),
    )
    title.pack(pady=20)

    # Subtitle
    subtitle = Label(
        ImageUI,
        text="Register New Student",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 18),
    )
    subtitle.pack(pady=10)

    # Enrollment No
    enrollment_label = Label(
        ImageUI,
        text="Enrollment No:",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 14),
    )
    enrollment_label.place(x=50, y=120)

    txt1 = Entry(
        ImageUI,
        width=20,
        bd=5,
        bg="#34495e",
        fg="#ecf0f1",
        relief=RIDGE,
        font=("Helvetica", 16),
        validate="key",
    )
    txt1.place(x=200, y=120)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Full Name
    name_label = Label(
        ImageUI,
        text="Full Name:",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 14),
    )
    name_label.place(x=50, y=180)

    txt2 = Entry(
        ImageUI,
        width=20,
        bd=5,
        bg="#34495e",
        fg="#ecf0f1",
        relief=RIDGE,
        font=("Helvetica", 16),
    )
    txt2.place(x=200, y=180)

    # Notification
    message = Label(
        ImageUI,
        text="",
        width=40,
        height=2,
        bg="#34495e",
        fg="#ecf0f1",
        relief=RIDGE,
        font=("Helvetica", 14),
    )
    message.place(x=50, y=240)

     # Buttons
    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    takeImg = Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=7,
        font=("Helvetica", 14),
        bg="#1abc9c",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=RIDGE,
    )
    takeImg.place(x=50, y=320)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    trainImg = Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=7,
        font=("Helvetica", 14),
        bg="#e67e22",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=RIDGE,
    )
    trainImg.place(x=300, y=320)
    
    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    trainImg = Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=7,
        font=("Helvetica", 14),
        bg="#e67e22",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=RIDGE,
    )
    trainImg.place(x=300, y=320)

window.mainloop()