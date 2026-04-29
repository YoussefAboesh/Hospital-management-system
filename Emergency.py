import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import sqlite3
from tkinter import messagebox

class Database:
    def __init__(self, data):
        self.con = sqlite3.connect(data)
        self.cur = self.con.cursor()
        
    def fetch_emergency_patients(self):
        self.cur.execute("SELECT DISTINCT name FROM Patients WHERE convert_to_dep = 'Emergency'")
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

db = Database("Patient.data")

root = tk.Tk()
root.title("Emergency Page")
root.geometry("1920x1080")
root.configure(bg="#2c3e50")

patient_name_label = tk.Label(root, text="Patient Name", bg="#2c3e50", fg="white", font=("Arial", 20))
patient_name_label.place(x=20, y=20)

patient_name_var = tk.StringVar()
patient_name_dropdown = ttk.Combobox(root, textvariable=patient_name_var, font=("Arial", 14))
patient_names = db.fetch_emergency_patients()  
patient_name_dropdown['values'] = patient_names
patient_name_dropdown.place(x=20, y=80)

title_label = tk.Label(root, text="Choose a procedure", bg="#2c3e50", fg="white", font=("Arial", 20))
title_label.pack(pady=20)

option_var = tk.StringVar(value="")
option_menu = ttk.Combobox(root, textvariable=option_var, font=("Arial", 14))
option_menu['values'] = ["Solution Suspension", "Injection", "Respirator"]
option_menu.pack(pady=10)

assigned_beds = [None, None, None]

def assign_bed():
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Combobox) or isinstance(widget, tk.Button):
            if widget != assign_button and widget != patient_name_dropdown and widget != option_menu:
                widget.destroy()

    selected_patient = patient_name_var.get()
    selected_action = option_var.get()
    if not selected_patient or not selected_action:
        messagebox.showerror("Error", "Please select patient name and procedure!")
        return

    bed_selection_var = tk.StringVar(value="")
    bed_selection_menu = ttk.Combobox(root, textvariable=bed_selection_var, font=("Arial", 14))
    bed_selection_menu['values'] = ["1", "2", "3"]
    bed_selection_menu.place(x=20, y=140)

    def confirm_bed():
        selected_bed = bed_selection_var.get()
        if not selected_bed:
            messagebox.showerror("Error", "Please select a bed!")
            return

        bed_index = int(selected_bed) - 1

        if assigned_beds[bed_index] is not None:
            messagebox.showerror("Error", f"Bed {selected_bed} is already occupied!")
            return

        assigned_beds[bed_index] = selected_patient
        bed_texts[bed_index].config(text=f"{selected_patient}\n{selected_action}")

        action_times = {"Injection": 20, "Solution Suspension": 40, "Respirator": 60}
        time_left = action_times.get(selected_action, 0)

        def countdown(bed_index, time_left):
            if time_left > 0:
                bed_texts[bed_index].config(text=f"{selected_patient}\n{selected_action}\n{time_left} Seconds")
                time_left -= 1
                root.after(1000, countdown, bed_index, time_left)
            else:
                bed_texts[bed_index].config(text=f"Bed {bed_index + 1}")
                assigned_beds[bed_index] = None
                

        countdown(bed_index, time_left)

    confirm_button = tk.Button(root, text="Confirm", command=confirm_bed, font=("Arial", 14), bg="white", fg="black")
    confirm_button.place(x=20, y=200)

assign_button = tk.Button(root, text="Choose a bed", command=assign_bed, font=("Arial", 14), bg="white", fg="black")
assign_button.place(x=20, y=240)



assign_button = tk.Button(root, text="Choose a bed", command=assign_bed, font=("Arial", 14), bg="white", fg="black")
assign_button.pack(pady=20)

beds_frame = tk.Frame(root, bg="#2c3e50")
beds_frame.pack(pady=30)

bed_labels = []
bed_texts = []

try:
    bed_image_path = r"media\bed1.png"
    bed_image = Image.open(bed_image_path)
    bed_image = bed_image.resize((300, 300))
    bed_photo = ImageTk.PhotoImage(bed_image)

    for i in range(3):
        bed_frame = tk.Frame(beds_frame, bg="#2c3e50")
        bed_frame.grid(row=0, column=i, padx=100)

        bed_label = tk.Label(bed_frame, image=bed_photo, bg="#2c3e50")
        bed_label.pack()
        bed_labels.append(bed_label)

        bed_text = tk.Label(bed_frame, text=f"Bed {i + 1}", bg="#2c3e50", fg="white", font=("Arial", 14))
        bed_text.pack()
        bed_texts.append(bed_text)
except Exception as e:
    error_label = tk.Label(beds_frame, text=f"Error loading image: {e}", bg="#2c3e50", fg="red")
    error_label.pack()

root.mainloop()
