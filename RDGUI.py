# import tkinter as tk
# from tkinter import ttk, messagebox
# import mysql.connector
# from dotenv import load_dotenv
# import os
# load_dotenv(dotenv_path='.env')

# # Establish connection with MySQL database
# def connect_db():
#     try:
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password = os.getenv('password'),
#             database='business_supply'
#         )
#         return conn
#     except mysql.connector.Error as err:
#         messagebox.showerror("Database Error", f"Error: {err}")
#         return None

# # Close connection with MySQL database
# def close_db(conn):
#     if conn:
#         conn.close()

# # Validate input fields
# def validate_fields(fields):
#     for field in fields:
#         if not field.get().strip():
#             messagebox.showerror("Validation Error", "All fields must be filled.")
#             return False
#     return True

# # Main application window
# class BusinessSupplyApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Business Supply System")
#         self.create_widgets()

#     def create_widgets(self):
#         # Tabs for different procedures
#         tab_control = ttk.Notebook(self.root)

#         self.add_owner_tab(tab_control)
#         self.add_business_tab(tab_control)
#         self.add_service_tab(tab_control)
#         self.add_location_tab(tab_control)
#         # Additional tabs...

#         tab_control.pack(expand=1, fill="both")

#     def add_location_tab(self, tab_control):
#         # Implement similarly to other tabs
#         # Placeholder for the add_location_tab method
#         tab = ttk.Frame(tab_control)
#         tab_control.add(tab, text="Add Location")

#         # Example fields; you should expand this based on your requirements
#         ttk.Label(tab, text="Location Label:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
#         location_label = ttk.Entry(tab)
#         location_label.grid(row=0, column=1, padx=10, pady=5)

#         ttk.Label(tab, text="X Coordinate:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
#         x_coord = ttk.Entry(tab)
#         x_coord.grid(row=1, column=1, padx=10, pady=5)

#         ttk.Label(tab, text="Y Coordinate:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
#         y_coord = ttk.Entry(tab)
#         y_coord.grid(row=2, column=1, padx=10, pady=5)

#         ttk.Label(tab, text="Space:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
#         space = ttk.Entry(tab)
#         space.grid(row=3, column=1, padx=10, pady=5)

#         def add_location():
#             if not validate_fields([location_label, x_coord, y_coord, space]):
#                 return
#             conn = connect_db()
#             if conn:
#                 cursor = conn.cursor()
#                 try:
#                     cursor.callproc('add_location', [
#                         location_label.get(),
#                         x_coord.get(),
#                         y_coord.get(),
#                         space.get()
#                     ])
#                     conn.commit()
#                     messagebox.showinfo("Success", "Location added successfully.")
#                     # Clear all entry fields
#                     location_label.delete(0, tk.END)
#                     x_coord.delete(0, tk.END)
#                     y_coord.delete(0, tk.END)
#                     space.delete(0, tk.END)
#                 except mysql.connector.Error as err:
#                     messagebox.showerror("Error", f"Failed to add location: {err}")
#                     print(f"Stored procedure error: {err}")
#                 finally:
#                     close_db(conn)

#         ttk.Button(tab, text="Add Location", command=add_location).grid(row=4, column=1, pady=10, sticky=tk.E)
#         ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=4, column=0, pady=10, sticky=tk.W)

#     def add_service_tab(self, tab_control):
#         # Create a new tab
#         tab = ttk.Frame(tab_control)
#         tab_control.add(tab, text="Add Service")

#         # Labels and Entry Widgets for Input Fields
#         ttk.Label(tab, text="Service ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
#         service_id = ttk.Entry(tab)
#         service_id.grid(row=0, column=1, padx=10, pady=5)

#         ttk.Label(tab, text="Service Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
#         service_name = ttk.Entry(tab)
#         service_name.grid(row=1, column=1, padx=10, pady=5)

#         ttk.Label(tab, text="Home Base:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
#         home_base = ttk.Entry(tab)
#         home_base.grid(row=2, column=1, padx=10, pady=5)

#         ttk.Label(tab, text="Manager Username:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
#         manager = ttk.Entry(tab)
#         manager.grid(row=3, column=1, padx=10, pady=5)

#         # Function to Add Service
#         def add_service():
#             # Validate all input fields are filled
#             if not validate_fields([service_id, service_name, home_base, manager]):
#                 return

#             # Establish Database Connection
#             conn = connect_db()
#             if conn:
#                 cursor = conn.cursor()
#                 try:
#                     # Call the 'add_service' stored procedure
#                     cursor.callproc('add_service', [
#                         service_id.get(),
#                         service_name.get(),
#                         home_base.get(),
#                         manager.get()
#                     ])
#                     conn.commit()
#                     messagebox.showinfo("Success", "Service added successfully.")

#                     # Clear all entry fields after successful addition
#                     service_id.delete(0, tk.END)
#                     service_name.delete(0, tk.END)
#                     home_base.delete(0, tk.END)
#                     manager.delete(0, tk.END)

#                 except mysql.connector.Error as err:
#                     messagebox.showerror("Error", f"Failed to add service: {err}")
#                     print(f"Stored procedure error: {err}")  # For debugging purposes

#                 finally:
#                     close_db(conn)

#         # Buttons for Adding Service and Canceling
#         ttk.Button(tab, text="Add Service", command=add_service).grid(row=4, column=1, pady=10, sticky=tk.E)
#         ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=4, column=0, pady=10, sticky=tk.W)


#     def add_owner_tab(self, tab_control):
#         tab = ttk.Frame(tab_control)
#         tab_control.add(tab, text="Add Owner")

#         ttk.Label(tab, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
#         first_name = ttk.Entry(tab)
#         first_name.grid(row=0, column=1)

#         ttk.Label(tab, text="Last Name:").grid(row=1, column=0, padx=10, pady=5)
#         last_name = ttk.Entry(tab)
#         last_name.grid(row=1, column=1)

#         ttk.Label(tab, text="Username:").grid(row=2, column=0, padx=10, pady=5)
#         username = ttk.Entry(tab)
#         username.grid(row=2, column=1)

#         ttk.Label(tab, text="Address:").grid(row=3, column=0, padx=10, pady=5)
#         address = ttk.Entry(tab)
#         address.grid(row=3, column=1)

#         ttk.Label(tab, text="Birthdate (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
#         birthdate = ttk.Entry(tab)
#         birthdate.grid(row=4, column=1)

#         def add_owner():
#             if not validate_fields([first_name, last_name, username, address, birthdate]):
#                 return
#             conn = connect_db()
#             if conn:
#                 cursor = conn.cursor()
#                 try:
#                     cursor.callproc('add_owner', [
#                         username.get(),
#                         first_name.get(),
#                         last_name.get(),
#                         address.get(),
#                         birthdate.get()
#                     ])
#                     conn.commit()
#                     messagebox.showinfo("Success", "Owner added successfully.")
#                     # Clear all entry fields
#                     first_name.delete(0, tk.END)
#                     last_name.delete(0, tk.END)
#                     username.delete(0, tk.END)
#                     address.delete(0, tk.END)
#                     birthdate.delete(0, tk.END)
#                 except mysql.connector.Error as err:
#                     messagebox.showerror("Error", f"Failed to add owner: {err}")
#                 finally:
#                     close_db(conn)

#         ttk.Button(tab, text="Add Owner", command=add_owner).grid(row=5, column=1, pady=10)
#         ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=5, column=0, pady=10)

#     # Add Business Tab
#     def add_business_tab(self, tab_control):
#         tab = ttk.Frame(tab_control)
#         tab_control.add(tab, text="Add Business")

#         ttk.Label(tab, text="Business Name:").grid(row=0, column=0, padx=10, pady=5)
#         business_name = ttk.Entry(tab)
#         business_name.grid(row=0, column=1)

#         ttk.Label(tab, text="Rating:").grid(row=1, column=0, padx=10, pady=5)
#         rating = ttk.Entry(tab)
#         rating.grid(row=1, column=1)

#         ttk.Label(tab, text="Spent:").grid(row=2, column=0, padx=10, pady=5)
#         spent = ttk.Entry(tab)
#         spent.grid(row=2, column=1)

#         ttk.Label(tab, text="Location:").grid(row=3, column=0, padx=10, pady=5)
#         location = ttk.Entry(tab)
#         location.grid(row=3, column=1)

#         def add_business():
#             if not validate_fields([business_name, rating, spent, location]):
#                 return
#             conn = connect_db()
#             if conn:
#                 cursor = conn.cursor()
#                 try:
#                     cursor.callproc('add_business', [
#                         business_name.get(),
#                         rating.get(),
#                         spent.get(),
#                         location.get()
#                     ])
#                     conn.commit()
#                     messagebox.showinfo("Success", "Business added successfully.")
#                     business_name.delete(0, tk.END)
#                     rating.delete(0, tk.END)
#                     spent.delete(0, tk.END)
#                     location.delete(0, tk.END)
#                 except mysql.connector.Error as err:
#                     messagebox.showerror("Error", f"Failed to add business: {err}")
#                 finally:
#                     close_db(conn)

#         ttk.Button(tab, text="Add Business", command=add_business).grid(row=4, column=1, pady=10)
#         ttk.Button(tab, text="Cancel", command=self.root.destroy).grid(row=4, column=0, pady=10)

#     # Additional

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = BusinessSupplyApp(root)
#     root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path='.env')

# Establish connection with MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv('password'),
            database='business_supply'
        )
        print("Database connection established.")
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        print(f"Database connection failed: {err}")
        return None

# Close connection with MySQL database
def close_db(conn):
    if conn:
        conn.close()
        print("Database connection closed.")

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
        # Tabs for different procedures and views
        tab_control = ttk.Notebook(self.root)

        # Stored Procedure Tabs
        self.add_owner_tab(tab_control)
        self.add_business_tab(tab_control)
        self.add_service_tab(tab_control)
        self.add_location_tab(tab_control)
        self.add_employee_tab(tab_control)
        self.add_driver_role_tab(tab_control)
        self.add_worker_role_tab(tab_control)
        self.add_product_tab(tab_control)
        self.add_van_tab(tab_control)
        self.start_funding_tab(tab_control)
        self.hire_employee_tab(tab_control)
        self.fire_employee_tab(tab_control)
        self.manage_service_tab(tab_control)
        self.takeover_van_tab(tab_control)
        self.load_van_tab(tab_control)
        self.refuel_van_tab(tab_control)
        self.drive_van_tab(tab_control)
        self.purchase_product_tab(tab_control)
        self.remove_product_tab(tab_control)
        self.remove_van_tab(tab_control)
        self.remove_driver_role_tab(tab_control)

        # View Display Tabs
        self.display_owner_view_tab(tab_control)
        self.display_employee_view_tab(tab_control)
        self.display_driver_view_tab(tab_control)
        self.display_location_view_tab(tab_control)
        self.display_product_view_tab(tab_control)
        self.display_service_view_tab(tab_control)

        tab_control.pack(expand=1, fill="both")

    # -------------------- Stored Procedure Tabs --------------------

    def add_owner_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Owner")

        # Input Fields
        ttk.Label(tab, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        first_name = ttk.Entry(tab)
        first_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Last Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        last_name = ttk.Entry(tab)
        last_name.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Username:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        username = ttk.Entry(tab)
        username.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Address:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        address = ttk.Entry(tab)
        address.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Birthdate (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        birthdate = ttk.Entry(tab)
        birthdate.grid(row=4, column=1, padx=10, pady=5)

        # Add Owner Function
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
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Owner", command=add_owner).grid(row=5, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([first_name, last_name, username, address, birthdate])).grid(row=5, column=0, pady=10, sticky=tk.W)

    def add_business_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Business")

        # Input Fields
        ttk.Label(tab, text="Business Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        business_name = ttk.Entry(tab)
        business_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Rating (1-5):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        rating = ttk.Entry(tab)
        rating.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Spent:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        spent = ttk.Entry(tab)
        spent.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Location:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        location = ttk.Entry(tab)
        location.grid(row=3, column=1, padx=10, pady=5)

        # Add Business Function
        def add_business():
            if not validate_fields([business_name, rating, spent, location]):
                return
            # Validate rating is between 1 and 5
            try:
                r = int(rating.get())
                if r < 1 or r > 5:
                    messagebox.showerror("Validation Error", "Rating must be between 1 and 5.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Rating must be an integer between 1 and 5.")
                return

            # Validate spent is an integer
            try:
                s = int(spent.get())
                if s < 0:
                    messagebox.showerror("Validation Error", "Spent must be a non-negative integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Spent must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_business', [
                        business_name.get(),
                        r,
                        s,
                        location.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Business added successfully.")
                    # Clear all entry fields
                    business_name.delete(0, tk.END)
                    rating.delete(0, tk.END)
                    spent.delete(0, tk.END)
                    location.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add business: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Business", command=add_business).grid(row=4, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([business_name, rating, spent, location])).grid(row=4, column=0, pady=10, sticky=tk.W)

    def add_service_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Service")

        # Input Fields
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

        # Add Service Function
        def add_service():
            if not validate_fields([service_id, service_name, home_base, manager]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_service', [
                        service_id.get(),
                        service_name.get(),
                        home_base.get(),
                        manager.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Service added successfully.")
                    # Clear all entry fields
                    service_id.delete(0, tk.END)
                    service_name.delete(0, tk.END)
                    home_base.delete(0, tk.END)
                    manager.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add service: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Service", command=add_service).grid(row=4, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([service_id, service_name, home_base, manager])).grid(row=4, column=0, pady=10, sticky=tk.W)

    def add_location_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Location")

        # Input Fields
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

        # Add Location Function
        def add_location():
            if not validate_fields([location_label, x_coord, y_coord, space]):
                return

            # Validate that X Coordinate, Y Coordinate, and Space are integers
            try:
                x = int(x_coord.get())
                y = int(y_coord.get())
                s = int(space.get())
                if s < 0:
                    messagebox.showerror("Validation Error", "Space must be a non-negative integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "X Coordinate, Y Coordinate, and Space must be integers.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_location', [
                        location_label.get(),
                        x,
                        y,
                        s
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

        # Buttons
        ttk.Button(tab, text="Add Location", command=add_location).grid(row=4, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([location_label, x_coord, y_coord, space])).grid(row=4, column=0, pady=10, sticky=tk.W)

    def add_employee_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Employee")

        # Input Fields
        ttk.Label(tab, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        username = ttk.Entry(tab)
        username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="First Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        first_name = ttk.Entry(tab)
        first_name.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Last Name:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        last_name = ttk.Entry(tab)
        last_name.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Address:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        address = ttk.Entry(tab)
        address.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Birthdate (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        birthdate = ttk.Entry(tab)
        birthdate.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Tax ID:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        tax_id = ttk.Entry(tab)
        tax_id.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Hired Date (YYYY-MM-DD):").grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)
        hired_date = ttk.Entry(tab)
        hired_date.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Experience (years):").grid(row=7, column=0, padx=10, pady=5, sticky=tk.E)
        experience = ttk.Entry(tab)
        experience.grid(row=7, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Salary:").grid(row=8, column=0, padx=10, pady=5, sticky=tk.E)
        salary = ttk.Entry(tab)
        salary.grid(row=8, column=1, padx=10, pady=5)

        # Add Employee Function
        def add_employee():
            fields = [username, first_name, last_name, address, birthdate, tax_id, hired_date, experience, salary]
            if not validate_fields(fields):
                return

            # Validate numerical fields
            try:
                exp = int(experience.get())
                sal = int(salary.get())
                if exp < 0 or sal < 0:
                    messagebox.showerror("Validation Error", "Experience and Salary must be non-negative integers.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Experience and Salary must be integers.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_employee', [
                        username.get(),
                        first_name.get(),
                        last_name.get(),
                        address.get(),
                        birthdate.get(),
                        tax_id.get(),
                        hired_date.get(),
                        exp,
                        sal
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Employee added successfully.")
                    # Clear all entry fields
                    for field in fields:
                        field.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add employee: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Employee", command=add_employee).grid(row=9, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([username, first_name, last_name, address, birthdate, tax_id, hired_date, experience, salary])).grid(row=9, column=0, pady=10, sticky=tk.W)

    def add_driver_role_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Driver Role")

        # Input Fields
        ttk.Label(tab, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        username = ttk.Entry(tab)
        username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="License ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        license_id = ttk.Entry(tab)
        license_id.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="License Type:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        license_type = ttk.Entry(tab)
        license_type.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Driver Experience (trips):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        driver_experience = ttk.Entry(tab)
        driver_experience.grid(row=3, column=1, padx=10, pady=5)

        # Add Driver Role Function
        def add_driver_role():
            if not validate_fields([username, license_id, license_type, driver_experience]):
                return

            # Validate driver experience is integer
            try:
                exp = int(driver_experience.get())
                if exp < 0:
                    messagebox.showerror("Validation Error", "Driver Experience must be a non-negative integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Driver Experience must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_driver_role', [
                        username.get(),
                        license_id.get(),
                        license_type.get(),
                        exp
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Driver role added successfully.")
                    # Clear all entry fields
                    username.delete(0, tk.END)
                    license_id.delete(0, tk.END)
                    license_type.delete(0, tk.END)
                    driver_experience.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add driver role: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Driver Role", command=add_driver_role).grid(row=4, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([username, license_id, license_type, driver_experience])).grid(row=4, column=0, pady=10, sticky=tk.W)

    def add_worker_role_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Worker Role")

        # Input Fields
        ttk.Label(tab, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        username = ttk.Entry(tab)
        username.grid(row=0, column=1, padx=10, pady=5)

        # Add Worker Role Function
        def add_worker_role():
            if not validate_fields([username]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_worker_role', [
                        username.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Worker role added successfully.")
                    # Clear the entry field
                    username.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add worker role: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Worker Role", command=add_worker_role).grid(row=1, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([username])).grid(row=1, column=0, pady=10, sticky=tk.W)

    def add_product_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Product")

        # Input Fields
        ttk.Label(tab, text="Barcode:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        barcode = ttk.Entry(tab)
        barcode.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Product Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        product_name = ttk.Entry(tab)
        product_name.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Weight:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        weight = ttk.Entry(tab)
        weight.grid(row=2, column=1, padx=10, pady=5)

        # Add Product Function
        def add_product():
            if not validate_fields([barcode, product_name, weight]):
                return

            # Validate weight is integer
            try:
                w = int(weight.get())
                if w < 0:
                    messagebox.showerror("Validation Error", "Weight must be a non-negative integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Weight must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_product', [
                        barcode.get(),
                        product_name.get(),
                        w
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Product added successfully.")
                    # Clear all entry fields
                    barcode.delete(0, tk.END)
                    product_name.delete(0, tk.END)
                    weight.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add product: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Product", command=add_product).grid(row=3, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([barcode, product_name, weight])).grid(row=3, column=0, pady=10, sticky=tk.W)

    def add_van_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Add Van")

        # Input Fields
        ttk.Label(tab, text="Service ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Tag:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        tag = ttk.Entry(tab)
        tag.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Fuel:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        fuel = ttk.Entry(tab)
        fuel.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Capacity:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        capacity = ttk.Entry(tab)
        capacity.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Sales:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        sales = ttk.Entry(tab)
        sales.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Driven By (Username):").grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        driven_by = ttk.Entry(tab)
        driven_by.grid(row=5, column=1, padx=10, pady=5)

        # Add Van Function
        def add_van():
            fields = [service_id, tag, fuel, capacity, sales]
            if not validate_fields(fields):
                return

            # Validate numerical fields
            try:
                t = int(tag.get())
                f = int(fuel.get())
                c = int(capacity.get())
                s = int(sales.get())
                if t < 0 or f < 0 or c < 0 or s < 0:
                    messagebox.showerror("Validation Error", "Tag, Fuel, Capacity, and Sales must be non-negative integers.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Tag, Fuel, Capacity, and Sales must be integers.")
                return

            # Driven By can be optional (NULL)
            driven_by_val = driven_by.get() if driven_by.get().strip() else None

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('add_van', [
                        service_id.get(),
                        t,
                        f,
                        c,
                        s,
                        driven_by_val
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Van added successfully.")
                    # Clear all entry fields
                    for field in fields:
                        field.delete(0, tk.END)
                    driven_by.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to add van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Add Van", command=add_van).grid(row=6, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([service_id, tag, fuel, capacity, sales, driven_by])).grid(row=6, column=0, pady=10, sticky=tk.W)

    def start_funding_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Start Funding")

        # Input Fields
        ttk.Label(tab, text="Owner Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        owner_username = ttk.Entry(tab)
        owner_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Amount:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        amount = ttk.Entry(tab)
        amount.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Business Name:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        business_name = ttk.Entry(tab)
        business_name.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Fund Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        fund_date = ttk.Entry(tab)
        fund_date.grid(row=3, column=1, padx=10, pady=5)

        # Start Funding Function
        def start_funding():
            if not validate_fields([owner_username, amount, business_name, fund_date]):
                return

            # Validate amount is integer
            try:
                amt = int(amount.get())
                if amt <= 0:
                    messagebox.showerror("Validation Error", "Amount must be a positive integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Amount must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('start_funding', [
                        owner_username.get(),
                        amt,
                        business_name.get(),
                        fund_date.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Funding started successfully.")
                    # Clear all entry fields
                    owner_username.delete(0, tk.END)
                    amount.delete(0, tk.END)
                    business_name.delete(0, tk.END)
                    fund_date.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to start funding: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Start Funding", command=start_funding).grid(row=4, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([owner_username, amount, business_name, fund_date])).grid(row=4, column=0, pady=10, sticky=tk.W)

    def hire_employee_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Hire Employee")

        # Input Fields
        ttk.Label(tab, text="Employee Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        employee_username = ttk.Entry(tab)
        employee_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Service ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=1, column=1, padx=10, pady=5)

        # Hire Employee Function
        def hire_employee():
            if not validate_fields([employee_username, service_id]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('hire_employee', [
                        employee_username.get(),
                        service_id.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Employee hired successfully.")
                    # Clear all entry fields
                    employee_username.delete(0, tk.END)
                    service_id.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to hire employee: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Hire Employee", command=hire_employee).grid(row=2, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([employee_username, service_id])).grid(row=2, column=0, pady=10, sticky=tk.W)

    def fire_employee_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Fire Employee")

        # Input Fields
        ttk.Label(tab, text="Employee Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        employee_username = ttk.Entry(tab)
        employee_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Service ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=1, column=1, padx=10, pady=5)

        # Fire Employee Function
        def fire_employee():
            if not validate_fields([employee_username, service_id]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('fire_employee', [
                        employee_username.get(),
                        service_id.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Employee fired successfully.")
                    # Clear all entry fields
                    employee_username.delete(0, tk.END)
                    service_id.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to fire employee: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Fire Employee", command=fire_employee).grid(row=2, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([employee_username, service_id])).grid(row=2, column=0, pady=10, sticky=tk.W)

    def manage_service_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Manage Service")

        # Input Fields
        ttk.Label(tab, text="Employee Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        employee_username = ttk.Entry(tab)
        employee_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Service ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=1, column=1, padx=10, pady=5)

        # Manage Service Function
        def manage_service():
            if not validate_fields([employee_username, service_id]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('manage_service', [
                        employee_username.get(),
                        service_id.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Service managed successfully.")
                    # Clear all entry fields
                    employee_username.delete(0, tk.END)
                    service_id.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to manage service: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Manage Service", command=manage_service).grid(row=2, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([employee_username, service_id])).grid(row=2, column=0, pady=10, sticky=tk.W)

    def takeover_van_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Takeover Van")

        # Input Fields
        ttk.Label(tab, text="Driver Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        driver_username = ttk.Entry(tab)
        driver_username.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Service ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Van Tag:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        van_tag = ttk.Entry(tab)
        van_tag.grid(row=2, column=1, padx=10, pady=5)

        # Takeover Van Function
        def takeover_van():
            if not validate_fields([driver_username, service_id, van_tag]):
                return

            # Validate van_tag is integer
            try:
                tag = int(van_tag.get())
                if tag < 0:
                    messagebox.showerror("Validation Error", "Van Tag must be a non-negative integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Van Tag must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('takeover_van', [
                        driver_username.get(),
                        service_id.get(),
                        tag
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Van takeover successful.")
                    # Clear all entry fields
                    driver_username.delete(0, tk.END)
                    service_id.delete(0, tk.END)
                    van_tag.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to takeover van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Takeover Van", command=takeover_van).grid(row=3, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([driver_username, service_id, van_tag])).grid(row=3, column=0, pady=10, sticky=tk.W)

    def load_van_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Load Van")

        # Input Fields
        ttk.Label(tab, text="Service ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Van Tag:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        van_tag = ttk.Entry(tab)
        van_tag.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Product Barcode:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        product_barcode = ttk.Entry(tab)
        product_barcode.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="More Packages:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        more_packages = ttk.Entry(tab)
        more_packages.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Price:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        price = ttk.Entry(tab)
        price.grid(row=4, column=1, padx=10, pady=5)

        # Load Van Function
        def load_van():
            if not validate_fields([service_id, van_tag, product_barcode, more_packages, price]):
                return

            # Validate numerical fields
            try:
                mp = int(more_packages.get())
                p = int(price.get())
                if mp <= 0 or p <= 0:
                    messagebox.showerror("Validation Error", "More Packages and Price must be positive integers.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "More Packages and Price must be integers.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('load_van', [
                        service_id.get(),
                        int(van_tag.get()),
                        product_barcode.get(),
                        mp,
                        p
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Van loaded successfully.")
                    # Clear all entry fields
                    service_id.delete(0, tk.END)
                    van_tag.delete(0, tk.END)
                    product_barcode.delete(0, tk.END)
                    more_packages.delete(0, tk.END)
                    price.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to load van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Load Van", command=load_van).grid(row=5, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([service_id, van_tag, product_barcode, more_packages, price])).grid(row=5, column=0, pady=10, sticky=tk.W)

    def refuel_van_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Refuel Van")

        # Input Fields
        ttk.Label(tab, text="Service ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Van Tag:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        van_tag = ttk.Entry(tab)
        van_tag.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="More Fuel:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        more_fuel = ttk.Entry(tab)
        more_fuel.grid(row=2, column=1, padx=10, pady=5)

        # Refuel Van Function
        def refuel_van():
            if not validate_fields([service_id, van_tag, more_fuel]):
                return

            # Validate more_fuel is integer
            try:
                mf = int(more_fuel.get())
                if mf <= 0:
                    messagebox.showerror("Validation Error", "More Fuel must be a positive integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "More Fuel must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('refuel_van', [
                        service_id.get(),
                        int(van_tag.get()),
                        mf
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Van refueled successfully.")
                    # Clear all entry fields
                    service_id.delete(0, tk.END)
                    van_tag.delete(0, tk.END)
                    more_fuel.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to refuel van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Refuel Van", command=refuel_van).grid(row=3, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([service_id, van_tag, more_fuel])).grid(row=3, column=0, pady=10, sticky=tk.W)

    def drive_van_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Drive Van")

        # Input Fields
        ttk.Label(tab, text="Service ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Van Tag:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        van_tag = ttk.Entry(tab)
        van_tag.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Destination Location:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        destination = ttk.Entry(tab)
        destination.grid(row=2, column=1, padx=10, pady=5)

        # Drive Van Function
        def drive_van():
            if not validate_fields([service_id, van_tag, destination]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('drive_van', [
                        service_id.get(),
                        int(van_tag.get()),
                        destination.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Van driven successfully.")
                    # Clear all entry fields
                    service_id.delete(0, tk.END)
                    van_tag.delete(0, tk.END)
                    destination.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to drive van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Drive Van", command=drive_van).grid(row=3, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([service_id, van_tag, destination])).grid(row=3, column=0, pady=10, sticky=tk.W)

    def purchase_product_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Purchase Product")

        # Input Fields
        ttk.Label(tab, text="Business Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        business_name = ttk.Entry(tab)
        business_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Service ID:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Van Tag:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        van_tag = ttk.Entry(tab)
        van_tag.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Product Barcode:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        product_barcode = ttk.Entry(tab)
        product_barcode.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Quantity:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        quantity = ttk.Entry(tab)
        quantity.grid(row=4, column=1, padx=10, pady=5)

        # Purchase Product Function
        def purchase_product():
            if not validate_fields([business_name, service_id, van_tag, product_barcode, quantity]):
                return

            # Validate quantity is integer
            try:
                q = int(quantity.get())
                if q <= 0:
                    messagebox.showerror("Validation Error", "Quantity must be a positive integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Quantity must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('purchase_product', [
                        business_name.get(),
                        service_id.get(),
                        int(van_tag.get()),
                        product_barcode.get(),
                        q
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Product purchased successfully.")
                    # Clear all entry fields
                    business_name.delete(0, tk.END)
                    service_id.delete(0, tk.END)
                    van_tag.delete(0, tk.END)
                    product_barcode.delete(0, tk.END)
                    quantity.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to purchase product: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Purchase Product", command=purchase_product).grid(row=5, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([business_name, service_id, van_tag, product_barcode, quantity])).grid(row=5, column=0, pady=10, sticky=tk.W)

    def remove_product_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Remove Product")

        # Input Fields
        ttk.Label(tab, text="Product Barcode:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        product_barcode = ttk.Entry(tab)
        product_barcode.grid(row=0, column=1, padx=10, pady=5)

        # Remove Product Function
        def remove_product():
            if not validate_fields([product_barcode]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('remove_product', [
                        product_barcode.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Product removed successfully.")
                    # Clear the entry field
                    product_barcode.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to remove product: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Remove Product", command=remove_product).grid(row=1, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([product_barcode])).grid(row=1, column=0, pady=10, sticky=tk.W)

    def remove_van_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Remove Van")

        # Input Fields
        ttk.Label(tab, text="Service ID:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        service_id = ttk.Entry(tab)
        service_id.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(tab, text="Van Tag:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        van_tag = ttk.Entry(tab)
        van_tag.grid(row=1, column=1, padx=10, pady=5)

        # Remove Van Function
        def remove_van():
            if not validate_fields([service_id, van_tag]):
                return

            # Validate van_tag is integer
            try:
                tag = int(van_tag.get())
                if tag < 0:
                    messagebox.showerror("Validation Error", "Van Tag must be a non-negative integer.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Van Tag must be an integer.")
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('remove_van', [
                        service_id.get(),
                        tag
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Van removed successfully.")
                    # Clear all entry fields
                    service_id.delete(0, tk.END)
                    van_tag.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to remove van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Remove Van", command=remove_van).grid(row=2, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([service_id, van_tag])).grid(row=2, column=0, pady=10, sticky=tk.W)

    def remove_driver_role_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Remove Driver Role")

        # Input Fields
        ttk.Label(tab, text="Driver Username:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        driver_username = ttk.Entry(tab)
        driver_username.grid(row=0, column=1, padx=10, pady=5)

        # Remove Driver Role Function
        def remove_driver_role():
            if not validate_fields([driver_username]):
                return

            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.callproc('remove_driver_role', [
                        driver_username.get()
                    ])
                    conn.commit()
                    messagebox.showinfo("Success", "Driver role removed successfully.")
                    # Clear the entry field
                    driver_username.delete(0, tk.END)
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to remove driver role: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        # Buttons
        ttk.Button(tab, text="Remove Driver Role", command=remove_driver_role).grid(row=1, column=1, pady=10, sticky=tk.E)
        ttk.Button(tab, text="Cancel", command=self.clear_fields([driver_username])).grid(row=1, column=0, pady=10, sticky=tk.W)

    # -------------------- View Display Tabs --------------------

    def display_owner_view_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Owner View")

        # Treeview Widget
        tree = ttk.Treeview(tab, columns=("Username", "First Name", "Last Name", "Address", "Birthdate",
                                         "Businesses Funded", "Locations", "Highest Rating",
                                         "Lowest Rating", "Total Debt"), show='headings')
        tree.heading("Username", text="Username")
        tree.heading("First Name", text="First Name")
        tree.heading("Last Name", text="Last Name")
        tree.heading("Address", text="Address")
        tree.heading("Birthdate", text="Birthdate")
        tree.heading("Businesses Funded", text="Businesses Funded")
        tree.heading("Locations", text="Locations")
        tree.heading("Highest Rating", text="Highest Rating")
        tree.heading("Lowest Rating", text="Lowest Rating")
        tree.heading("Total Debt", text="Total Debt")

        tree.pack(expand=True, fill="both")

        # Load Owner View Data
        def load_owner_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute("SELECT * FROM display_owner_view")
                    rows = cursor.fetchall()
                    # Clear existing data
                    for item in tree.get_children():
                        tree.delete(item)
                    # Insert new data
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("username"),
                            row.get("first_name"),
                            row.get("last_name"),
                            row.get("address"),
                            row.get("birthdate"),
                            row.get("businesses_funded"),
                            row.get("locations"),
                            row.get("highest_rating"),
                            row.get("lowest_rating"),
                            row.get("total_debt")
                        ))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to load owner view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        # Load Button
        ttk.Button(tab, text="Load View", command=load_owner_view).pack(pady=10)

    def display_employee_view_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Employee View")

        # Treeview Widget
        tree = ttk.Treeview(tab, columns=("Username", "Tax ID", "Salary", "Hired Date", "Experience",
                                         "License ID", "Driver Experience", "Is Manager"), show='headings')
        tree.heading("Username", text="Username")
        tree.heading("Tax ID", text="Tax ID")
        tree.heading("Salary", text="Salary")
        tree.heading("Hired Date", text="Hired Date")
        tree.heading("Experience", text="Experience")
        tree.heading("License ID", text="License ID")
        tree.heading("Driver Experience", text="Driver Experience")
        tree.heading("Is Manager", text="Is Manager")

        tree.pack(expand=True, fill="both")

        # Load Employee View Data
        def load_employee_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute("SELECT * FROM display_employee_view")
                    rows = cursor.fetchall()
                    # Clear existing data
                    for item in tree.get_children():
                        tree.delete(item)
                    # Insert new data
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("username"),
                            row.get("tax_identifier"),
                            row.get("salary"),
                            row.get("hiring_date"),
                            row.get("experience_level"),
                            row.get("license_identifier"),
                            row.get("drivering_experience"),
                            row.get("is_manager")
                        ))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to load employee view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        # Load Button
        ttk.Button(tab, text="Load View", command=load_employee_view).pack(pady=10)

    def display_driver_view_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Driver View")

        # Treeview Widget
        tree = ttk.Treeview(tab, columns=("Username", "License ID", "Driving Experience", "Vans Controlled"), show='headings')
        tree.heading("Username", text="Username")
        tree.heading("License ID", text="License ID")
        tree.heading("Driving Experience", text="Driving Experience")
        tree.heading("Vans Controlled", text="Vans Controlled")

        tree.pack(expand=True, fill="both")

        # Load Driver View Data
        def load_driver_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute("SELECT * FROM display_driver_view")
                    rows = cursor.fetchall()
                    # Clear existing data
                    for item in tree.get_children():
                        tree.delete(item)
                    # Insert new data
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("username"),
                            row.get("licenseID"),
                            row.get("drivering_experience"),
                            row.get("vans_controlled")
                        ))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to load driver view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        # Load Button
        ttk.Button(tab, text="Load View", command=load_driver_view).pack(pady=10)

    def display_location_view_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Location View")

        # Treeview Widget
        tree = ttk.Treeview(tab, columns=("Label", "X Coord", "Y Coord", "Long Name",
                                         "Number of Vans", "Van IDs", "Capacity", "Remaining Capacity"), show='headings')
        tree.heading("Label", text="Label")
        tree.heading("X Coord", text="X Coord")
        tree.heading("Y Coord", text="Y Coord")
        tree.heading("Long Name", text="Long Name")
        tree.heading("Number of Vans", text="Number of Vans")
        tree.heading("Van IDs", text="Van IDs")
        tree.heading("Capacity", text="Capacity")
        tree.heading("Remaining Capacity", text="Remaining Capacity")

        tree.pack(expand=True, fill="both")

        # Load Location View Data
        def load_location_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute("SELECT * FROM display_location_view")
                    rows = cursor.fetchall()
                    # Clear existing data
                    for item in tree.get_children():
                        tree.delete(item)
                    # Insert new data
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("label"),
                            row.get("x_coord"),
                            row.get("y_coord"),
                            row.get("long_name"),
                            row.get("num_vans"),
                            row.get("van_ids"),
                            row.get("capacity"),
                            row.get("remaining_capacity")
                        ))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to load location view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        # Load Button
        ttk.Button(tab, text="Load View", command=load_location_view).pack(pady=10)

    def display_product_view_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Product View")

        # Treeview Widget
        tree = ttk.Treeview(tab, columns=("Product Name", "Location", "Amount Available", "Low Price", "High Price"), show='headings')
        tree.heading("Product Name", text="Product Name")
        tree.heading("Location", text="Location")
        tree.heading("Amount Available", text="Amount Available")
        tree.heading("Low Price", text="Low Price")
        tree.heading("High Price", text="High Price")

        tree.pack(expand=True, fill="both")

        # Load Product View Data
        def load_product_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute("SELECT * FROM display_product_view")
                    rows = cursor.fetchall()
                    # Clear existing data
                    for item in tree.get_children():
                        tree.delete(item)
                    # Insert new data
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("product_name"),
                            row.get("located_at"),
                            row.get("amount_available"),
                            row.get("low_price"),
                            row.get("high_price")
                        ))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to load product view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        # Load Button
        ttk.Button(tab, text="Load View", command=load_product_view).pack(pady=10)

    def display_service_view_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text="Service View")

        # Treeview Widget
        tree = ttk.Treeview(tab, columns=("Service ID", "Service Name", "Home Base", "Manager",
                                         "Revenue", "Products Carried", "Cost Carried", "Weight Carried"), show='headings')
        tree.heading("Service ID", text="Service ID")
        tree.heading("Service Name", text="Service Name")
        tree.heading("Home Base", text="Home Base")
        tree.heading("Manager", text="Manager")
        tree.heading("Revenue", text="Revenue")
        tree.heading("Products Carried", text="Products Carried")
        tree.heading("Cost Carried", text="Cost Carried")
        tree.heading("Weight Carried", text="Weight Carried")

        tree.pack(expand=True, fill="both")

        # Load Service View Data
        def load_service_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute("SELECT * FROM display_service_view")
                    rows = cursor.fetchall()
                    # Clear existing data
                    for item in tree.get_children():
                        tree.delete(item)
                    # Insert new data
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("id"),
                            row.get("long_name"),
                            row.get("home_base"),
                            row.get("manager"),
                            row.get("revenue"),
                            row.get("products_carried"),
                            row.get("cost_carried"),
                            row.get("weight_carried")
                        ))
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to load service view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        # Load Button
        ttk.Button(tab, text="Load View", command=load_service_view).pack(pady=10)

    # -------------------- Utility Methods --------------------

    def clear_fields(self, fields):
        # Returns a function to clear multiple entry fields
        def clear():
            for field in fields:
                field.delete(0, tk.END)
        return clear

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessSupplyApp(root)
    root.mainloop()

