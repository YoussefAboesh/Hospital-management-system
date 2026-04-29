import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

conn = sqlite3.connect("hospital_staff.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nationality TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS nurses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nationality TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

doctors = [
    ("Dr. Ahmed Hossam", "Egyptian", 40),
    ("Dr. Nouran Saeed", "Egyptian", 35),
    ("Dr. Youssef Khalil", "Egyptian", 45),
    ("Dr. Mariam Adel", "Egyptian", 30),
    ("Dr. Omar Tarek", "Egyptian", 50)
]

nurses = [
    ("Nurse Rana Samir", "Egyptian", 28),
    ("Nurse Khaled Anwar", "Egyptian", 32),
    ("Nurse Salma Nabil", "Egyptian", 25)
]

cursor.executemany("""
INSERT INTO doctors (name, nationality, age)
SELECT ?, ?, ? 
WHERE NOT EXISTS (
    SELECT 1 FROM doctors WHERE name = ?
)
""", [(d[0], d[1], d[2], d[0]) for d in doctors])

cursor.executemany("""
INSERT INTO nurses (name, nationality, age)
SELECT ?, ?, ? 
WHERE NOT EXISTS (
    SELECT 1 FROM nurses WHERE name = ?
)
""", [(n[0], n[1], n[2], n[0]) for n in nurses])

conn.commit()

root = tk.Tk()
root.title("Hospital Staff Management")
root.geometry("1920x1080")
root.config(bg="#2c3e50")

def show_doctors_and_nurses():
    for row in doctor_tree.get_children():
        doctor_tree.delete(row)
    
    cursor.execute("SELECT * FROM doctors")
    doctors_data = cursor.fetchall()
    for row in doctors_data:
        doctor_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

    for row in nurse_tree.get_children():
        nurse_tree.delete(row)
    
    cursor.execute("SELECT * FROM nurses")
    nurses_data = cursor.fetchall()
    for row in nurses_data:
        nurse_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))

def add_doctor():
    name = name_entry.get()
    nationality = nationality_entry.get()
    age = age_entry.get()
    
    if not name or not nationality or not age:
        messagebox.showerror("Input Error", "Please fill all fields!")
        return
    
    cursor.execute("INSERT INTO doctors (name, nationality, age) VALUES (?, ?, ?)", (name, nationality, int(age)))
    conn.commit()
    show_doctors_and_nurses()
    messagebox.showinfo("Success", "Doctor added successfully!")

def add_nurse():
    name = name_entry.get()
    nationality = nationality_entry.get()
    age = age_entry.get()
    
    if not name or not nationality or not age:
        messagebox.showerror("Input Error", "Please fill all fields!")
        return
    
    cursor.execute("INSERT INTO nurses (name, nationality, age) VALUES (?, ?, ?)", (name, nationality, int(age)))
    conn.commit()
    show_doctors_and_nurses()
    messagebox.showinfo("Success", "Nurse added successfully!")

def delete_doctor():
    selected_doctor = doctor_tree.selection()
    if not selected_doctor:
        messagebox.showerror("Selection Error", "Please select a doctor to delete.")
        return

    doctor_id = doctor_tree.item(selected_doctor[0])['values'][0]
    cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    conn.commit()
    show_doctors_and_nurses()
    messagebox.showinfo("Success", "Doctor deleted successfully!")

def delete_nurse():
    selected_nurse = nurse_tree.selection()
    if not selected_nurse:
        messagebox.showerror("Selection Error", "Please select a nurse to delete.")
        return

    nurse_id = nurse_tree.item(selected_nurse[0])['values'][0]
    cursor.execute("DELETE FROM nurses WHERE id = ?", (nurse_id,))
    conn.commit()
    show_doctors_and_nurses()
    messagebox.showinfo("Success", "Nurse deleted successfully!")

frame = tk.Frame(root, bg="#2c3e50")
frame.pack(pady=10)

name_label = tk.Label(frame, text="Name", bg="#2c3e50",fg="white", font=("Arial", 14))
name_label.grid(row=0, column=0)
name_entry = tk.Entry(frame, font=("Arial", 14))
name_entry.grid(row=0, column=1)

nationality_label = tk.Label(frame, text="Nationality", bg="#2c3e50",fg="white", font=("Arial", 14))
nationality_label.grid(row=1, column=0)
nationality_entry = tk.Entry(frame, font=("Arial", 14))
nationality_entry.grid(row=1, column=1)

age_label = tk.Label(frame, text="Age", bg="#2c3e50",fg="white", font=("Arial", 14))
age_label.grid(row=2, column=0)
age_entry = tk.Entry(frame, font=("Arial", 14))
age_entry.grid(row=2, column=1)

add_doctor_button = tk.Button(frame, text="Add Doctor", command=add_doctor, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=20, height=2)
add_doctor_button.grid(row=3, column=0, pady=10)

add_nurse_button = tk.Button(frame, text="Add Nurse", command=add_nurse, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", width=20, height=2)
add_nurse_button.grid(row=3, column=1, pady=10)

doctor_label = tk.Label(root, text="Doctors Table",fg="white", font=("Arial", 16, "bold"), bg="#2c3e50")
doctor_label.pack(pady=5)
doctor_tree = ttk.Treeview(root, columns=("ID", "Name", "Nationality", "Age"), show="headings", height=8)
doctor_tree.heading("ID", text="ID")
doctor_tree.heading("Name", text="Name")
doctor_tree.heading("Nationality", text="Nationality")
doctor_tree.heading("Age", text="Age")
doctor_tree.pack(pady=10)

nurse_label = tk.Label(root, text="Nurses Table",fg="white", font=("Arial", 16, "bold"), bg="#2c3e50")
nurse_label.pack(pady=5)
nurse_tree = ttk.Treeview(root, columns=("ID", "Name", "Nationality", "Age"), show="headings", height=8)
nurse_tree.heading("ID", text="ID")
nurse_tree.heading("Name", text="Name")
nurse_tree.heading("Nationality", text="Nationality")
nurse_tree.heading("Age", text="Age")
nurse_tree.pack(pady=10)

delete_doctor_button = tk.Button(root, text="Delete Doctor", command=delete_doctor, font=("Arial", 14, "bold"), bg="#FF5733", fg="white", width=20, height=2)
delete_doctor_button.pack(pady=5)

delete_nurse_button = tk.Button(root, text="Delete Nurse", command=delete_nurse, font=("Arial", 14, "bold"), bg="#FF5733", fg="white", width=20, height=2)
delete_nurse_button.pack(pady=5)

show_doctors_and_nurses()

def on_close():
    conn.close()
    root.quit()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
