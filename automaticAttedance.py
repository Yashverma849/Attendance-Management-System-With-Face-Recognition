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
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/TrainingImageLabel/Trainner.yml"
)
trainimage_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/TrainingImage"
studentdetail_path = (
    "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/StudentDetails/studentdetails.csv"
)
attendance_path = "c:/Users/verma/Desktop/Attendance-Management-system-using-face-recognition-master/Attendance"

def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train the model"
                    Notifica.configure(
                        text=e,
                        bg="#2c3e50",
                        fg="#e74c3c",
                        width=33,
                        font=("Helvetica", 14, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully for " + Subject
                Notifica.configure(
                    text=m,
                    bg="#1abc9c",
                    fg="#ecf0f1",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("Helvetica", 14, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="#2c3e50")
                cs = os.path.join(path, fileName)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="#ecf0f1",
                                font=("Helvetica", 12, "bold"),
                                bg="#34495e",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c, padx=5, pady=5)
                            c += 1
                        r += 1
                root.mainloop()
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    subject = Tk()
    subject.title("Subject Attendance")
    subject.geometry("700x400")
    subject.resizable(0, 0)
    subject.configure(background="#2c3e50")

    # Add logo
    try:
        logo = Image.open("UI_Image/logo.png")  # Replace with your logo path
        logo = logo.resize((60, 60), Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(subject, image=logo_img, bg="#2c3e50")
        logo_label.image = logo_img
        logo_label.place(x=10, y=10)
    except Exception as e:
        print("Logo not found:", e)

    # Title
    title = tk.Label(
        subject,
        text="Attendance Management System",
        bg="#2c3e50",
        fg="#1abc9c",
        font=("Helvetica", 24, "bold"),
    )
    title.pack(pady=20)

    # Subtitle
    subtitle = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 18),
    )
    subtitle.pack(pady=10)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    sub_label = tk.Label(
        subject,
        text="Enter Subject:",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 14),
    )
    sub_label.place(x=50, y=150)

    tx = tk.Entry(
        subject,
        width=20,
        bd=5,
        bg="#34495e",
        fg="#ecf0f1",
        relief=tk.RIDGE,
        font=("Helvetica", 16),
    )
    tx.place(x=200, y=150)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("Helvetica", 14),
        bg="#1abc9c",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=tk.RIDGE,
    )
    fill_a.place(x=200, y=220)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("Helvetica", 14),
        bg="#e67e22",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=tk.RIDGE,
    )
    attf.place(x=400, y=220)

    subject.mainloop()