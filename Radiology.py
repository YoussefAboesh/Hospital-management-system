import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os
import sqlite3

class Database:
    def __init__(self, data):
        self.con = sqlite3.connect(data)
        self.cur = self.con.cursor()
        
        sql = """
        CREATE TABLE IF NOT EXISTS Patients(
            id INTEGER PRIMARY KEY,
            name text,
            age text,
            gender text,
            blood text,
            chronic_dis text,
            convert_to_dep text,
            phone text,
            address text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def fetch_emergency_patients(self):
        self.cur.execute("SELECT DISTINCT name FROM Patients WHERE convert_to_dep = 'X-Ray'")
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

db = Database("Patient.data")

def update_patient_list():
    emergency_patients = db.fetch_emergency_patients()
    patient_name['values'] = emergency_patients 

def show_patient_details(event):
    selected_patient_name = patient_name.get()
    if selected_patient_name:
        cursor = db.con.cursor()
        cursor.execute("""
            SELECT id, name, age, gender, blood, phone, address
            FROM Patients
            WHERE name=?
        """, (selected_patient_name,))
        result = cursor.fetchone()
        if result:
            patient_id, name, age, gender, blood, phone, address = result
            details_label.config(
                text=(
                    f"ID: {patient_id}\n"
                    f"Name: {name}\n"
                    f"Age: {age}\n"
                    f"Gender: {gender}\n"
                    f"Blood Type: {blood}\n"
                    f"Phone: {phone}\n"
                    f"Address: {address}"
                )
            )

def show_xray_image():
    selected_xray = xray_type.get()
    if selected_xray:

        folder_path = f"xray_images/{selected_xray}"
        if os.path.exists(folder_path):
            images = os.listdir(folder_path)
            if images:
                random_image = random.choice(images)
                image_path = os.path.join(folder_path, random_image)

                img = Image.open(image_path)
                img = img.resize((400, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                image_label.config(image=photo)
                image_label.image = photo
                return

root = tk.Tk()
root.title("X-Ray Department")
root.geometry("1920x1080")
root.configure(bg="#2c3e50")

patient_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
patient_frame.place(x=50, y=50, width=300, height=200)

patient_label = tk.Label(patient_frame, text="Patient Name:", font=("Arial", 12), bg="white")
patient_label.pack(pady=10)

patient_name = ttk.Combobox(patient_frame, width=25)
patient_name.pack(pady=10)

patient_name.bind("<<ComboboxSelected>>", show_patient_details)

details_label = tk.Label(patient_frame, text="", font=("Arial", 10), bg="white", justify="left")
details_label.pack(pady=10)

update_patient_list()

xray_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
xray_frame.place(relx=0.5, rely=0.3, anchor="center", width=300, height=200)

xray_label = tk.Label(xray_frame, text="X-Ray Type:", font=("Arial", 12), bg="white")
xray_label.pack(pady=10)

xray_type = tk.StringVar()
xray_options = ["leg", "knee", "hand", "chest", "xray"]
xray_dropdown = ttk.Combobox(xray_frame, values=xray_options, textvariable=xray_type, width=25)
xray_dropdown.pack(pady=10)

show_button = tk.Button(xray_frame, text="Show X-Ray", command=show_xray_image)
show_button.pack(pady=10)

image_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
image_frame.place(relx=0.5, rely=0.7, anchor="center", width=400, height=400)

image_label = tk.Label(image_frame, bg="white")
image_label.pack(expand=True, fill="both")

root.mainloop()
