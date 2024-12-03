import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Establish connection with MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_pass',
            database='business_supply'
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Close connection with MySQL database
def close_db(conn):
    if conn:
        conn.close()

# Validate input fields
def validate_fields(fields):
    for field in fields:
        if not field.get().strip():
            messagebox.showerror("Validation Error", "All fields must be filled.")
            return False
    return True

# Main application window
class BusinessSupplyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Supply System")
        self.create_widgets()

    def create_widgets(self):
        # Tabs for different procedures
        tab_control = ttk.Notebook(self.root)

        self.add_owner_tab(tab_control)
        self.add_business_tab(tab_control)
        self.add_service_tab(tab_control)
        self.add_location_tab(tab_control)
        # Additional tabs...

        tab_control.pack(expand=1, fill="both")

    def add_owner_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Owner")

        ttk.Label(tab, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
        first_name = ttk.Entry(tab)
        first_name.grid(row=0, column=1)

        ttk.Label(tab, text="Last Name:").grid(row=1, column=0, padx=10, pady=5)
        last_name = ttk.Entry(tab)
        last_name.grid(row=1, column=1)

        ttk.Label(tab, text="Username:").grid(row=2, column=0, padx=10, pady=5)
        username = ttk.Entry(tab)
        username.grid(row=2, column=1)

        ttk.Label(tab, text="Address:").grid(row=3, column=0, padx=10, pady=5)
        address = ttk.Entry(tab)
        address.grid(row=3, column=1)

        ttk.Label(tab, text="Birthdate (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
        birthdate = ttk.Entry(tab)
        birthdate.grid(row=4, column=1)

        def add_owner():
            if not validate_fields([first_name, last_name, username, address, birthdate]):
                return
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_owner', [
                        username.get(),
                        first_name.get(),
                        last_name.get(),
                        address.get(),
                        birthdate.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Owner added successfully.")
                    # Clear all entry fields
                    first_name.delete(0, tk.END)
                    last_name.delete(0, tk.END)
                    username.delete(0, tk.END)
                    address.delete(0, tk.END)
                    birthdate.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add owner: {err}")
                finally:
                    close_db(conn)

        ttk.Button(tab, text="Add Owner", command=add_owner).grid(row=5, column=1, pady=10)
        ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=5, column=0, pady=10)

    # Add Business Tab
    def add_business_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Business")

        ttk.Label(tab, text="Business Name:").grid(row=0, column=0, padx=10, pady=5)
        business_name = ttk.Entry(tab)
        business_name.grid(row=0, column=1)

        ttk.Label(tab, text="Rating:").grid(row=1, column=0, padx=10, pady=5)
        rating = ttk.Entry(tab)
        rating.grid(row=1, column=1)

        ttk.Label(tab, text="Spent:").grid(row=2, column=0, padx=10, pady=5)
        spent = ttk.Entry(tab)
        spent.grid(row=2, column=1)

        ttk.Label(tab, text="Location:").grid(row=3, column=0, padx=10, pady=5)
        location = ttk.Entry(tab)
        location.grid(row=3, column=1)

        def add_business():
            if not validate_fields([business_name, rating, spent, location]):
                return
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_business', [
                        business_name.get(),
                        rating.get(),
                        spent.get(),
                        location.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Business added successfully.")
                    business_name.delete(0, tk.END)
                    rating.delete(0, tk.END)
                    spent.delete(0, tk.END)
                    location.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add business: {err}")
                finally:
                    close_db(conn)

        ttk.Button(tab, text="Add Business", command=add_business).grid(row=4, column=1, pady=10)
        ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=4, column=0, pady=10)

    # Additional