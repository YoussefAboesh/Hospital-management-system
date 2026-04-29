import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess  

def create_background(window, image_path):
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(window, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading background image: {e}")

def create_title_frame(window, title_text):
    title_frame = tk.Frame(window, bg="#2c3e50", height=100, width=1920)  
    title_frame.pack(fill="x")
    title_label = tk.Label(
        title_frame,
        text=title_text,
        font=("Helvetica", 36, "bold"),
        fg="white",  
        bg="#2c3e50"  
    )
    title_label.pack(pady=20)

def main_window():
    root = tk.Tk()
    root.title("Hospital System")
    root.geometry("1920x1080")

    create_background(root, r"media\bg9.jpg")

    create_title_frame(root, "Hospital System")

    welcome_label = tk.Label(
        root,
        text="Welcome to Our Hospital Management System!",
        font=("Helvetica", 24, "bold"),  
        fg="#00334e", 
        bg="#e6f7ff" 
    )
    welcome_label.pack(pady=30)

    features_frame = tk.Frame(root, bg="#e6f7ff")
    features_frame.pack(pady=20)

    features = [
        "🏥 Comprehensive Healthcare Services for All Ages",
        "🩺 24/7 Emergency and Radiology Support",
        "👩‍⚕️ Experienced and Compassionate Medical Staff",
        "📈 Advanced Medical Technology and Equipment",
        "🌟 Comfortable and Clean Facilities"
    ]

    for feature in features:
        tk.Label(
            features_frame,
            text=feature,
            font=("Helvetica", 20, "italic"),
            fg="#005073", 
            bg="#e6f7ff" 
        ).pack(anchor="w", padx=100, pady=5)

    # زر لعرض الأقسام
    departments_button = tk.Button(
        root,
        text="View Departments and Managements",
        font=("Helvetica", 20, "bold"), 
        bg="#2c3e50", 
        fg="white",  
        width=30,
        height=2,
        relief="raised",  
        command=departments_window
    )
    departments_button.pack(pady=50)

    root.mainloop()

def departments_window():
    departments = tk.Toplevel()
    departments.title("Departments and Managements")
    departments.geometry("1920x1080")

    create_background(departments, r"media\bg8.jpg")

    create_title_frame(departments, "Departments and Managements")

    tk.Button(
        departments,
        text="Departments",
        font=("Helvetica", 20, "bold"),
        bg="#57b8c7",  
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=department_window
    ).pack(pady=30)

    tk.Button(
        departments,
        text="Managements",
        font=("Helvetica", 20, "bold"),
        bg="#77c9d4",  
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=Managements_window 
    ).pack(pady=30)


def department_window():
      department = tk.Toplevel()
      department.title("Departments")
      department.geometry("1920x1080")
 
      create_background(department, r"media\bg8.jpg")

      create_title_frame(department, "Departments")

      tk.Button(
        department,
        text="Emergency",
        font=("Helvetica", 20, "bold"),
        bg="#57b8c7",  
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=lambda: open_python_file("Emergency.py")  
    ).pack(pady=30) 

      tk.Button(
        department,
        text="Radiology",
        font=("Helvetica", 20, "bold"),
        bg="#57b8c7",  
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=lambda: open_python_file("Radiology.py") 
    ).pack(pady=30) 
    
      tk.Button(
        department,
        text="Surgery",
        font=("Helvetica", 20, "bold"),
        bg="#57b8c7",  
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=lambda: open_python_file("Surgery.py")  
    ).pack(pady=30)
      
def Managements_window():
    Managements = tk.Toplevel()
    Managements.title("Managements")
    Managements.geometry("1920x1080")

    create_background(Managements,r"media\bg8.jpg")

    create_title_frame(Managements, "Managements")

    tk.Button(
        Managements,
        text="Nursing",
        font=("Helvetica", 20, "bold"),
        bg="#57b8c7", 
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=lambda: open_python_file("main.py")
    ).pack(pady=30) 

    tk.Button(
        Managements,
        text="Worker",
        font=("Helvetica", 20, "bold"),
        bg="#57b8c7",  
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=lambda: open_python_file("worker.py")  
    ).pack(pady=30) 
    
    tk.Button(
        Managements,
        text="Inventory",
        font=("Helvetica", 20, "bold"),
        bg="#57b8c7", 
        fg="white",
        width=20,
        height=2,
        relief="raised",
        command=lambda: open_python_file("Inventory.py")  
    ).pack(pady=30)

def open_python_file(file_path):
    try:
        subprocess.run(["python", file_path], check=True)
    except Exception as e:
        print(f"Error opening Python file: {e}")

if __name__ == "__main__":
    main_window()
