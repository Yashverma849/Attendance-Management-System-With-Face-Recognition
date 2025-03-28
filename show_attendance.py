import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk  # For adding logo

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
        if not filenames:
            t = f"No attendance files found for subject: {Subject}"
            text_to_speech(t)
            return

        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        root = tkinter.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="#2c3e50")  # Updated background color
        cs = f"Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(
                        root,
                        width=15,
                        height=2,
                        fg="#ecf0f1",  # Updated text color
                        font=("Helvetica", 12, "bold"),
                        bg="#34495e",  # Updated cell background color
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c, padx=5, pady=5)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    subject.title("Subject Attendance")
    subject.geometry("700x400")
    subject.resizable(0, 0)
    subject.configure(background="#2c3e50")  # Updated background color

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
        text="Which Subject of Attendance?",
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

    # Input field
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
        relief=RIDGE,
        font=("Helvetica", 16),
    )
    tx.place(x=200, y=150)

    # Buttons
    view_button = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("Helvetica", 14),
        bg="#1abc9c",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=RIDGE,
    )
    view_button.place(x=200, y=220)

    check_button = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("Helvetica", 14),
        bg="#e67e22",
        fg="#ecf0f1",
        height=2,
        width=15,
        relief=RIDGE,
    )
    check_button.place(x=400, y=220)

    subject.mainloop()