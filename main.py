from tkinter import *
from tkinter import ttk
from tkinter import messagebox


from data import Database
data = Database("Patient.data")

root = Tk()
root.title('Patient Management System')
root.geometry('1520x830')
root.resizable(False, False)
root.configure(bg='#2c3e50')

name = StringVar()
age = StringVar()
gender = StringVar()
blood = StringVar()
chronic_dis = StringVar()
convert_to_dep = StringVar()
phone = StringVar()

logo = PhotoImage(file=r'media\logo.png')
lbl_logo = Label(root, image=logo, bg='#2c3e50')
lbl_logo.place(x=20, y=620)

# ======================= Entries Frame =======================================
entries_frame = Frame(root, bg='#2c3e50')
entries_frame.place(x=1, y=1, width=330, height=640)
title = Label(entries_frame, text='Patient Entries', font=('Calibri', 18, 'bold'), bg='#2c3e50', fg='white')
title.place(x=45, y=5)

patname = Label(entries_frame, text='Name', font=('Calibri', 15), bg='#2c3e50', fg='white')
patname.place(x=15, y=50)
txtname = Entry(entries_frame, textvariable=name, width=20, font=('Calibri', 15))
txtname.place(x=100, y=54)

patage = Label(entries_frame, text='Age', font=('Calibri', 15), bg='#2c3e50', fg='white')
patage.place(x=20, y=100)
txtage = Entry(entries_frame, textvariable=age, width=20, font=('Calibri', 15))
txtage.place(x=100, y=105)

patgender = Label(entries_frame, text='Gender', font=('Calibri', 15), bg='#2c3e50', fg='white')
patgender.place(x=10, y=155)
combogender = ttk.Combobox(entries_frame, textvariable=gender, state='readonly', width=17, font=('Calibri', 16))
combogender['values'] = ("Male", "Female")
combogender.place(x=100, y=155)

patblod = Label(entries_frame, text='Blood T', font=('Calibri', 15), bg='#2c3e50', fg='white')
patblod.place(x=10, y=210)
comboblod = ttk.Combobox(entries_frame, textvariable=blood, state='readonly', width=17, font=('Calibri', 16))
comboblod['values'] = ("O", "AB", "A", "B")
comboblod.place(x=100, y=210)

patchronic = Label(entries_frame, text='Chronic Diseases :', font=('Calibri', 15), bg='#2c3e50', fg='white')
patchronic.place(x=10, y=255)
combochronic = ttk.Combobox(entries_frame, textvariable=chronic_dis, state='readonly', width=17, font=('Calibri', 16))
combochronic['values'] = ("Nothing", "Diabetes", "Blood Pressure", "Heart Disease", "Blood Fluidity")
combochronic.place(x=100, y=286)

patdep = Label(entries_frame, text='Convert To Department :', font=('Calibri', 15), bg='#2c3e50', fg='white')
patdep.place(x=10, y=330)
combodep = ttk.Combobox(entries_frame, textvariable=convert_to_dep, state='readonly', width=17, font=('Calibri', 16))
combodep['values'] = ("X-Ray", "Emergency", "Surgery")
combodep.place(x=100, y=358)

patphon = Label(entries_frame, text='Phone', font=('Calibri', 15), bg='#2c3e50', fg='white')
patphon.place(x=10, y=405)
txtphone = Entry(entries_frame, textvariable=phone, width=20, font=('Calibri', 15))
txtphone.place(x=100, y=410)

patadres = Label(entries_frame, text='Address :', font=('Calibri', 15), bg='#2c3e50', fg='white')
patadres.place(x=10, y=445)
txtaddress = Text(entries_frame, width=30, height=2, font=('Calibri', 15))
txtaddress.place(x=10, y=475)

# ================== define ================================

hide_frame = Frame(root, bg='#2c3e50')
hide_frame.place(x=331, y=1, width=1190, height=830)

def hide():
    hide_frame.lift()

def show():
    tree_frame.lift()
    

btn_hide = Button(entries_frame, text='Hide', bg='white', bd=1, relief=SOLID, cursor='hand2', command=hide)
btn_hide.place(x=220, y=10)

btn_show = Button(entries_frame, text='Show', bg='white', bd=1, relief=SOLID, cursor='hand2', command=show)
entries_frame.place(x=1, y=1, width=330, height=640)
btn_show.place(x=270, y=10)

def getdata(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    name.set(row[1])
    age.set(row[2])
    gender.set(row[3])
    blood.set(row[4])
    chronic_dis.set(row[5])
    convert_to_dep.set(row[6])
    phone.set(row[7])
    txtaddress.delete(1.0, END)
    txtaddress.insert(END, row[8])

def displayAll():
    tv.delete(*tv.get_children()) 
    for row in data.fetch():  
        tv.insert("", END, values=row)  

def clear():  
    name.set("")
    age.set("")
    gender.set("")
    blood.set("")
    chronic_dis.set("")
    convert_to_dep.set("")
    phone.set("")
    txtaddress.delete(1.0, END)

def delete():
    if not row:  
        messagebox.showerror("Error", "Please select a patient to delete")
        return
    
    data.remove(row[0])  
    clear()
    displayAll()

def add_Patient():
    if txtname.get() == "" or txtage.get() == "" or combogender.get() == "" or comboblod.get() == "" or combochronic.get() == "" or combodep.get() == "" or txtphone.get() == "" or txtaddress.get(1.0, END)== "":
        messagebox.showerror("Error !", "Please Fill All The Entry")
        return
    data.insert(
        txtname.get(),
        txtage.get(),
        combogender.get(),
        comboblod.get(),
        combochronic.get(),
        combodep.get(),
        txtphone.get(),
        txtaddress.get(1.0, END))
    
    messagebox.showinfo("Success", "Added New Patient")
    clear()
    displayAll()

def update():
    if txtname.get() == "" or txtage.get() == "" or combogender.get() == "" or comboblod.get() == "" or combochronic.get() == "" or combodep.get() == "" or txtphone.get() == "" or txtaddress.get(1.0, END).strip() == "":
        messagebox.showerror("Error !", "Please Fill All The Entry")
        return
    
    data.update(row[0],  
              txtname.get(),
              txtage.get(),
              combogender.get(),
              comboblod.get(),
              combochronic.get(),
              combodep.get(),
              txtphone.get(),
              txtaddress.get(1.0, END))
    
    messagebox.showinfo('Success', 'The Patient Data Is Updated')
    clear()
    displayAll()

# ================== buttons =================================
btn_fram = Frame(entries_frame, bg='#2c3e50', bd=1, relief=SOLID)
btn_fram.place(x=5, y=540, width=335, height=100)

btnADD = Button(btn_fram,
                text='ADD Details',
                width=14,
                height=1,
                font=('Calibri', 15),
                fg='white',
                bg='#16a085',
                bd=0,
                command=add_Patient,
                cursor='hand2'
                ).place(x=4, y=5)

btnEdit = Button(btn_fram,
                 text='Update Details',
                 width=14,
                 height=1,
                 font=('Calibri', 15),
                 fg='white',
                 bg='#2980b9',
                 bd=0,
                 cursor='hand2',
                 command=update
                 ).place(x=4, y=50)

btnDelete = Button(btn_fram,
                   text='Delete Details',
                   width=14,
                   height=1,
                   font=('Calibri', 15),
                   fg='white',
                   bg='#c0392b',
                   bd=0,
                   cursor='hand2',
                   command=delete
                   ).place(x=160, y=5)

btnClear = Button(btn_fram,
                  text='Clear Details',
                  width=14,
                  height=1,
                  font=('Calibri', 15),
                  fg='white',
                  bg='#f39c12',
                  bd=0,
                  cursor='hand2',
                  command=clear
                  ).place(x=160, y=50)

# ======================== table frame ===================================
tree_frame = Frame(root, bg='white')
tree_frame.place(x=330, y=1, width=1200, height=830)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 20), rowheight=50)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 20))

tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column("1", width="40")

tv.heading("2", text="Name")
tv.column("2", width="140")

tv.heading("3", text="Age")
tv.column("3", width="50")

tv.heading("4", text="Gender")
tv.column("4", width="90")

tv.heading("5", text="Blood Type")
tv.column("5", width="60")

tv.heading("6", text="Chronic Diseases")
tv.column("6", width="190")

tv.heading("7", text="Department")
tv.column("7", width="130")

tv.heading("8", text="Phone")
tv.column("8", width="150")

tv.heading("9", text="Address")
tv.column("9", width="190")

tv['show'] = 'headings'

tv.bind("<ButtonRelease-1>", getdata)

tv.place(x=2, y=1, height=829, width=1200)

displayAll()

#========================================= lopy frame ====================================
hide_frame = Frame(root, bg='#2c3e50')
hide_frame.place(x=331, y=1, width=1190, height=830)
urgent = PhotoImage(file=r'media\urgent.png')
lbl_urgent = Label(hide_frame, image= urgent, bg='#2c3e50')
lbl_urgent.place(x=0, y=0)
root.mainloop()
