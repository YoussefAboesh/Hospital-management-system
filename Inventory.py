from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

conn = sqlite3.connect("modern_inventory.db")
cursor = conn.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    manufacturer TEXT
)
""")

cursor.execute("PRAGMA foreign_keys=off;")
cursor.execute("""
PRAGMA table_info(medicines);
""")
columns = cursor.fetchall()

if not any(column[1] == "manufacturer" for column in columns):
    cursor.execute("""
    ALTER TABLE medicines ADD COLUMN manufacturer TEXT;
    """)
cursor.execute("PRAGMA foreign_keys=on;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL
)
""")
conn.commit()
#################################################   MAIN WINDOW   #####################################################
def main_window():
    root = Tk()
    root.title("Medicines Management System")
    root.geometry("1920x1080")
    root.configure(bg="#f7f7f7")

    title_label = Label(root, text="Inventory Management System", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#2c3e50")
    title_label.pack(pady=20)

    buttons_frame = Frame(root, bg="#f7f7f7")
    buttons_frame.pack(pady=20)

    Button(buttons_frame, text="View Medicines", font=("Arial", 16), bg="#5cb3ff", fg="white", 
           command=view_medicines_window, width=20, height=2).grid(row=0, column=0, padx=20, pady=10)

    Button(buttons_frame, text="Generate Receipt", font=("Arial", 16), bg="#5cb3ff", fg="white", 
           command=generate_receipt_window, width=20, height=2).grid(row=0, column=1, padx=20, pady=10)

    Button(buttons_frame, text="Search Medicines", font=("Arial", 16), bg="#5cb3ff", fg="white", 
           command=search_medicines_window, width=20, height=2).grid(row=0, column=2, padx=20, pady=10)

    Button(buttons_frame, text="Sell Medicines", font=("Arial", 16), bg="#5cb3ff", fg="white", 
           command=sell_medicines_window, width=20, height=2).grid(row=1, column=2, padx=20, pady=10)
    
    Button(buttons_frame, text="Add Medicines", font=("Arial", 16), bg="#5cb3ff", fg="white", 
           command=Add_medicines_window, width=20, height=2).grid(row=1, column=0, padx=20, pady=10)
    
    Button(buttons_frame, text="Edit Medicines", font=("Arial", 16), bg="#5cb3ff", fg="white", 
       command=edit_medicine_window, width=20, height=2).grid(row=1, column=1, padx=20, pady=10)


    root.mainloop()
#################################################   view medicines   #####################################################

def view_medicines_window():
    view_window = Toplevel()
    view_window.title("View Medicines")
    view_window.geometry("1450x400+50+350")

    tree = ttk.Treeview(view_window, columns=("ID", "Name", "Price", "Quantity", "Manufacturer"), show="headings")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Manufacturer", text="Manufacturer")

    cursor.execute("SELECT * FROM medicines")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

#################################################   search medicines   #####################################################

def search_medicines_window():
    search_window = Toplevel()
    search_window.title("Search Medicines")
    search_window.geometry("1450x400+50+350")
    search_window.configure(bg="#2c3e50")


    Label(search_window, text="Enter Medicine Name:",bg="#2c3e50", fg="white", font=("Arial", 14)).pack(pady=10)
    search_entry = Entry(search_window, font=("Arial", 14))
    search_entry.pack(pady=10)

    result_label = Label(search_window, text="", font=("Arial", 14),bg="#2c3e50", fg="white")
    result_label.pack(pady=10)

    def search_medicine():
        medicine_name = search_entry.get()
        cursor.execute("SELECT * FROM medicines WHERE name LIKE ?", ('%' + medicine_name + '%',))
        rows = cursor.fetchall()
        if rows:
            result = "\n".join([f"{row[1]} - ${row[2]} - {row[3]} in stock - Manufacturer: {row[4]}" for row in rows])
            result_label.config(text=result)
        else:
            result_label.config(text="No medicines found.")

    Button(search_window, text="Search", font=("Arial", 14), command=search_medicine).pack(pady=10)

#################################################   SELL medicines   #####################################################

def sell_medicines_window():
    sell_window = Toplevel()
    sell_window.title("Sell Medicines")
    sell_window.geometry("1450x400+50+350")
    sell_window.configure(bg="#2c3e50")

    Label(sell_window, text="Select Medicine:", font=("Arial", 14),bg="#2c3e50", fg="white").pack(pady=10)
    medicine_combobox = ttk.Combobox(sell_window, font=("Arial", 14), width=30)
    medicine_combobox.pack(pady=10)

    Label(sell_window, text="Enter Quantity:", font=("Arial", 14),bg="#2c3e50", fg="white").pack(pady=10)
    quantity_entry = Entry(sell_window, font=("Arial", 14))
    quantity_entry.pack(pady=10)

    total_price_label = Label(sell_window, text="Total Price: $0.00", font=("Arial", 16),bg="#2c3e50", fg="white")
    total_price_label.pack(pady=10)

    cursor.execute("SELECT name FROM medicines")
    medicines = [row[0] for row in cursor.fetchall()]
    medicine_combobox["values"] = medicines

    def calculate_total_price():
        try:
            medicine_name = medicine_combobox.get()
            quantity = int(quantity_entry.get())

            cursor.execute("SELECT price, quantity FROM medicines WHERE name = ?", (medicine_name,))
            result = cursor.fetchone()
            if result:
                price, stock_quantity = result
                if quantity > stock_quantity:
                    messagebox.showerror("Error", "Not enough stock available.")
                    return
                total_price = price * quantity
                total_price_label.config(text=f"Total Price: ${total_price:.2f}")
                return total_price, quantity, medicine_name, stock_quantity
            else:
                messagebox.showerror("Error", "Medicine not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity.")

    def sell_medicine():
        result = calculate_total_price()
        if result:
            total_price, quantity, medicine_name, stock_quantity = result
            new_quantity = stock_quantity - quantity

            cursor.execute("UPDATE medicines SET quantity = ? WHERE name = ?", (new_quantity, medicine_name))
            conn.commit()

            cursor.execute("INSERT INTO sales (medicine_name, quantity, total_price) VALUES (?, ?, ?)",
                           (medicine_name, quantity, total_price))
            conn.commit()

            messagebox.showinfo("Success", "Medicine sold successfully!")
            total_price_label.config(text="Total Price: $0.00")
            quantity_entry.delete(0, END)

    Button(sell_window, text="Calculate Total", font=("Arial", 14), command=calculate_total_price).pack(pady=10)
    Button(sell_window, text="Sell", font=("Arial", 14), bg="#28a745", fg="white", command=sell_medicine).pack(pady=10)

#################################################   generate_eceipt   #####################################################

def generate_receipt_window():
    receipt_window = Toplevel()
    receipt_window.title("Sales Receipt")
    receipt_window.geometry("1450x400+50+350")
    receipt_window.configure(bg="#2c3e50")


    tree = ttk.Treeview(receipt_window, columns=("ID", "Medicine", "Quantity", "Total Price"), show="headings")
    tree.pack(fill="both", expand=True, padx=20, pady=20)

    tree.heading("ID", text="ID")
    tree.heading("Medicine", text="Medicine")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Total Price", text="Total Price")

    cursor.execute("SELECT * FROM sales")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

#################################################   ADD medicines   #####################################################

def Add_medicines_window():
    add_window = Toplevel()
    add_window.title("Add Medicine")
    add_window.geometry("1450x450+50+350")

    Label(add_window, text="Medicine Name:", font=("Arial", 14)).pack(pady=10)
    medicine_name_entry = Entry(add_window, font=("Arial", 14))
    medicine_name_entry.pack(pady=10)

    Label(add_window, text="Price:", font=("Arial", 14)).pack(pady=10)
    price_entry = Entry(add_window, font=("Arial", 14))
    price_entry.pack(pady=10)

    Label(add_window, text="Quantity:", font=("Arial", 14)).pack(pady=10)
    quantity_entry = Entry(add_window, font=("Arial", 14))
    quantity_entry.pack(pady=10)

    Label(add_window, text="Manufacturer:", font=("Arial", 14)).pack(pady=10)
    manufacturer_entry = Entry(add_window, font=("Arial", 14))
    manufacturer_entry.pack(pady=10)

    def add_medicine():
        medicine_name = medicine_name_entry.get().strip()
        price = price_entry.get().strip()
        quantity = quantity_entry.get().strip()
        manufacturer = manufacturer_entry.get().strip()

        if not medicine_name or not price or not quantity or not manufacturer:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            price = float(price)
            quantity = int(quantity)
            if price <= 0 or quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and quantity.")
            return

        cursor.execute("INSERT INTO medicines (name, price, quantity, manufacturer) VALUES (?, ?, ?, ?)",
                       (medicine_name, price, quantity, manufacturer))
        conn.commit()

        messagebox.showinfo("Success", "Medicine added successfully!")
        add_window.destroy()

    Button(add_window, text="Add Medicine", font=("Arial", 14), bg="#28a745", fg="white", command=add_medicine).pack(pady=10)

#################################################   EDIT medicines   #####################################################

def edit_medicine_window():
    edit_window = Toplevel()
    edit_window.title("Edit Medicine")
    edit_window.geometry("1450x450+50+350")

    Label(edit_window, text="Select Medicine to Edit:", font=("Arial", 14)).pack(pady=10)
    
    medicine_combobox = ttk.Combobox(edit_window, font=("Arial", 14), width=30)
    medicine_combobox.pack(pady=10)

    cursor.execute("SELECT name FROM medicines")
    medicines = [row[0] for row in cursor.fetchall()]
    medicine_combobox["values"] = medicines

    Label(edit_window, text="New Price:", font=("Arial", 14)).pack(pady=10)
    price_entry = Entry(edit_window, font=("Arial", 14))
    price_entry.pack(pady=10)

    Label(edit_window, text="New Quantity:", font=("Arial", 14)).pack(pady=10)
    quantity_entry = Entry(edit_window, font=("Arial", 14))
    quantity_entry.pack(pady=10)

    Label(edit_window, text="New Manufacturer:", font=("Arial", 14)).pack(pady=10)
    manufacturer_entry = Entry(edit_window, font=("Arial", 14))
    manufacturer_entry.pack(pady=10)

    def update_medicine():
        medicine_name = medicine_combobox.get()
        new_price = price_entry.get().strip()
        new_quantity = quantity_entry.get().strip()
        new_manufacturer = manufacturer_entry.get().strip()

        if not medicine_name or not new_price or not new_quantity or not new_manufacturer:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            new_price = float(new_price)
            new_quantity = int(new_quantity)
            if new_price <= 0 or new_quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid price and quantity.")
            return
        
        cursor.execute("""
            UPDATE medicines 
            SET price = ?, quantity = ?, manufacturer = ?
            WHERE name = ?
        """, (new_price, new_quantity, new_manufacturer, medicine_name))
        conn.commit()

        messagebox.showinfo("Success", f"Medicine {medicine_name} updated successfully!")
        edit_window.destroy()

    Button(edit_window, text="Update Medicine",font=("Arial", 14), bg="#28a745", fg="white", command=update_medicine).pack(pady=10)
     

if __name__ == "__main__":
    main_window()
