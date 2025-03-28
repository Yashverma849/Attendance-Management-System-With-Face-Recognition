import tkinter as tk
from tkinter import Message, Text
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

ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")
d = {}
index = 0

#### GUI for manually filling attendance
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.title("Enter Subject Name")
    sb.geometry("700x400")
    sb.resizable(0, 0)
    sb.configure(background="#2c3e50")  # Updated background color

    # Add logo
    try:
        logo = Image.open("UI_Image/logo.png")  # Replace with your logo path
        logo = logo.resize((60, 60), Image.ANTIALIAS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(sb, image=logo_img, bg="#2c3e50")
        logo_label.image = logo_img
        logo_label.place(x=10, y=10)
    except Exception as e:
        print("Logo not found:", e)

    # Title
    title = tk.Label(
        sb,
        text="Attendance Management System",
        bg="#2c3e50",
        fg="#1abc9c",
        font=("Helvetica", 24, "bold"),
    )
    title.pack(pady=20)

    # Subtitle
    subtitle = tk.Label(
        sb,
        text="Enter Subject Name to Fill Attendance",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 18),
    )
    subtitle.pack(pady=10)

    def err_screen_for_subject():
        def ec_delete():
            ec.destroy()

        global ec
        ec = tk.Tk()
        ec.geometry("300x100")
        ec.title("Warning!!")
        ec.configure(background="#2c3e50")
        tk.Label(
            ec,
            text="Please enter subject name!!!",
            fg="#e74c3c",
            bg="#ecf0f1",
            font=("Helvetica", 14, "bold"),
        ).pack(pady=10)
        tk.Button(
            ec,
            text="OK",
            command=ec_delete,
            fg="#ecf0f1",
            bg="#1abc9c",
            width=10,
            font=("Helvetica", 12, "bold"),
        ).pack(pady=5)

    def fill_attendance():
        global subb
        subb = SUB_ENTRY.get()

        if subb == "":
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.title("Manually Attendance of " + str(subb))
            MFW.geometry("880x470")
            MFW.configure(background="#2c3e50")

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry("330x100")
                errsc2.title("Warning!!")
                errsc2.configure(background="#2c3e50")
                tk.Label(
                    errsc2,
                    text="Please enter Student & Enrollment!!!",
                    fg="#e74c3c",
                    bg="#ecf0f1",
                    font=("Helvetica", 14, "bold"),
                ).pack(pady=10)
                tk.Button(
                    errsc2,
                    text="OK",
                    command=del_errsc2,
                    fg="#ecf0f1",
                    bg="#1abc9c",
                    width=10,
                    font=("Helvetica", 12, "bold"),
                ).pack(pady=5)

            def testVal(inStr, acttyp):
                if acttyp == "1":  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(
                MFW,
                text="Enter Enrollment",
                width=20,
                height=2,
                fg="#ecf0f1",
                bg="#34495e",
                font=("Helvetica", 14, "bold"),
            )
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(
                MFW,
                text="Enter Student Name",
                width=20,
                height=2,
                fg="#ecf0f1",
                bg="#34495e",
                font=("Helvetica", 14, "bold"),
            )
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(
                MFW,
                width=20,
                bg="#34495e",
                fg="#ecf0f1",
                font=("Helvetica", 16),
            )
            ENR_ENTRY.place(x=290, y=110)

            STUDENT_ENTRY = tk.Entry(
                MFW,
                width=20,
                bg="#34495e",
                fg="#ecf0f1",
                font=("Helvetica", 16),
            )
            STUDENT_ENTRY.place(x=290, y=210)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            def enter_data_DB():
                global index
                global d
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == "":
                    err_screen1()
                elif STUDENT == "":
                    err_screen1()
                else:
                    if index == 0:
                        d = {
                            index: {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                        }
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")
                    else:
                        d[index] = {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")
                print(d)

            def create_csv():
                df = pd.DataFrame(d)
                csv_name = (
                    "Attendance(Manually)/"
                    + subb
                    + "_"
                    + Date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                df.to_csv(csv_name)
                O = "CSV created Successfully"
                Notifi.configure(
                    text=O,
                    bg="#1abc9c",
                    fg="#ecf0f1",
                    width=33,
                    font=("Helvetica", 14, "bold"),
                )
                Notifi.place(x=180, y=380)

            Notifi = tk.Label(
                MFW,
                text="CSV created Successfully",
                bg="#1abc9c",
                fg="#ecf0f1",
                width=33,
                height=2,
                font=("Helvetica", 14, "bold"),
            )

            c1ear_enroll = tk.Button(
                MFW,
                text="Clear",
                command=remove_enr,
                fg="#ecf0f1",
                bg="#e74c3c",
                width=10,
                height=1,
                font=("Helvetica", 12, "bold"),
            )
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(
                MFW,
                text="Clear",
                command=remove_student,
                fg="#ecf0f1",
                bg="#e74c3c",
                width=10,
                height=1,
                font=("Helvetica", 12, "bold"),
            )
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(
                MFW,
                text="Enter Data",
                command=enter_data_DB,
                fg="#ecf0f1",
                bg="#1abc9c",
                width=15,
                height=2,
                font=("Helvetica", 14, "bold"),
            )
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(
                MFW,
                text="Convert to CSV",
                command=create_csv,
                fg="#ecf0f1",
                bg="#e74c3c",
                width=15,
                height=2,
                font=("Helvetica", 14, "bold"),
            )
            MAKE_CSV.place(x=370, y=300)

            MFW.mainloop()

    # Input field
    sub_label = tk.Label(
        sb,
        text="Enter Subject:",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 14),
    )
    sub_label.place(x=50, y=150)

    SUB_ENTRY = tk.Entry(
        sb,
        width=20,
        bd=5,
        bg="#34495e",
        fg="#ecf0f1",
        relief=tk.RIDGE,
        font=("Helvetica", 16),
    )
    SUB_ENTRY.place(x=200, y=150)

    # Buttons
    fill_manual_attendance = tk.Button(
        sb,
        text="Fill Attendance",
        command=fill_attendance,
        bd=7,
        font=("Helvetica", 14),
        bg="#1abc9c",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=tk.RIDGE,
    )
    fill_manual_attendance.place(x=200, y=220)

    sb.mainloop()