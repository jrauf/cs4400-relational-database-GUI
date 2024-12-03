import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='.env')

# Establish connection with MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password = os.getenv('password'),
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

    def add_location_tab(self, tab_control):
        # Implement similarly to other tabs
        # Placeholder for the add_location_tab method
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Location")

        # Example fields; you should expand this based on your requirements
        ttk.Label(tab, text="Location Label:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        location_label = ttk.Entry(tab)
        location_label.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="X Coordinate:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        x_coord = ttk.Entry(tab)
        x_coord.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Y Coordinate:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        y_coord = ttk.Entry(tab)
        y_coord.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Space:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        space = ttk.Entry(tab)
        space.grid(row=3, column=1, padx=10, pady=5)

        def add_location():
            if not validate_fields([location_label, x_coord, y_coord, space]):
                return
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_location', [
                        location_label.get(),
                        x_coord.get(),
                        y_coord.get(),
                        space.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Location added successfully.")
                    # Clear all entry fields
                    location_label.delete(0, tk.END)
                    x_coord.delete(0, tk.END)
                    y_coord.delete(0, tk.END)
                    space.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add location: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        ttk.Button(tab, text="Add Location", command=add_location).grid(row=4, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=4, column=0, pady=10, sticky=tk.W)

    def add_service_tab(self, tab_control):
        # Create a new tab
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Service")

        # Labels and Entry Widgets for Input Fields
        ttk.Label(tab, text="Service ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Service Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        service_name = ttk.Entry(tab)
        service_name.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Home Base:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        home_base = ttk.Entry(tab)
        home_base.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Manager Username:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        manager = ttk.Entry(tab)
        manager.grid(row=3, column=1, padx=10, pady=5)

        # Function to Add Service
        def add_service():
            # Validate all input fields are filled
            if not validate_fields([service_id, service_name, home_base, manager]):
                return

            # Establish Database Connection
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    # Call the 'add_service' stored procedure
                    cursor.callproc('add_service', [
                        service_id.get(),
                        service_name.get(),
                        home_base.get(),
                        manager.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Service added successfully.")

                    # Clear all entry fields after successful addition
                    service_id.delete(0, tk.END)
                    service_name.delete(0, tk.END)
                    home_base.delete(0, tk.END)
                    manager.delete(0, tk.END)

                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add service: {err}")
                    print(f"Stored procedure error: {err}")  # For debugging purposes

                finally:
                    close_db(conn)

        # Buttons for Adding Service and Canceling
        ttk.Button(tab, text="Add Service", command=add_service).grid(row=4, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=4, column=0, pady=10, sticky=tk.W)


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

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessSupplyApp(root)
    root.mainloop()
