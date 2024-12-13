import tkinter as tk
from tkinter import ttk, messagebox
import os
import pymysql

def connect_db():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='admin1234',
            database='business_supply',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Database connection established.")
        return conn
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def close_db(conn):
    if conn:
        conn.close()
        print("Database connection closed.")

def validate_fields(fields):
    for field in fields:
        if not field.get().strip():
            messagebox.showerror("Validation Error", "All fields must be filled.")
            return False
    return True

class BusinessSupplyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Supply System")
        self.root.geometry("1400x800")
        self.create_widgets()

    def create_widgets(self):
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(paned, width=300, relief=tk.SUNKEN)
        paned.add(self.left_frame, weight=1)

        self.right_frame = ttk.Frame(paned, relief=tk.SUNKEN)
        paned.add(self.right_frame, weight=4)

        self.setup_navigation()

    def setup_navigation(self):
        self.nav_tree = ttk.Treeview(self.left_frame)
        self.nav_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        procedures_node = self.nav_tree.insert("", "end", text="Stored Procedures", open=True)
        views_node = self.nav_tree.insert("", "end", text="Views", open=True)
        tables_node = self.nav_tree.insert("", "end", text="Tables", open=True)  # NEW: Tables section

        self.stored_procedures = [
            "Add Owner",
            "Add Business",
            "Add Service",
            "Add Location",
            "Add Employee",
            "Add Driver Role",
            "Add Worker Role",
            "Add Product",
            "Add Van",
            "Start Funding",
            "Hire Employee",
            "Fire Employee",
            "Manage Service",
            "Takeover Van",
            "Load Van",
            "Refuel Van",
            "Drive Van",
            "Purchase Product",
            "Remove Product",
            "Remove Van",
            "Remove Driver Role"
        ]

        self.views = [
            "Display Owner View",
            "Display Employee View",
            "Display Driver View",
            "Display Location View",
            "Display Product View",
            "Display Service View"
        ]

        # NEW: List of tables from the given database schema
        self.tables = [
            "users",
            "employees",
            "business_owners",
            "drivers",
            "workers",
            "products",
            "locations",
            "businesses",
            "delivery_services",
            "vans",
            "contain",
            "work_for",
            "fund"
        ]

        for proc in self.stored_procedures:
            self.nav_tree.insert(procedures_node, "end", text=proc)

        for view in self.views:
            self.nav_tree.insert(views_node, "end", text=view)

        # NEW: Insert tables into the Tables node
        for table in self.tables:
            self.nav_tree.insert(tables_node, "end", text=table)

        scrollbar = ttk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.nav_tree.yview)
        self.nav_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.nav_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_tree_select(self, event):
        selected_item = self.nav_tree.focus()
        item_text = self.nav_tree.item(selected_item, "text")
        parent = self.nav_tree.parent(selected_item)
        parent_text = self.nav_tree.item(parent, "text") if parent else ""

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        if parent_text == "Stored Procedures":
            method_name = f"{self.format_method_name(item_text)}_form"
            method = getattr(self, method_name, None)
            if method:
                method()
            else:
                self.show_message(f"No form implemented for {item_text}")
        elif parent_text == "Views":
            core_name = item_text.replace("Display ", "").replace(" View", "")
            method_name = f"display_{self.format_method_name(core_name)}_view"
            method = getattr(self, method_name, None)
            if method:
                method()
            else:
                self.show_message(f"No display implemented for {item_text}")
        elif parent_text == "Tables":  # NEW: Handle table selection
            self.display_table(item_text)

    def format_method_name(self, text):
        return text.lower().replace(" ", "_")

    def show_message(self, message):
        messagebox.showinfo("Information", message)

    # -------------------- Stored Procedure Forms --------------------
    def add_owner_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Owner", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="First Name:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        first_name = ttk.Entry(form_frame)
        first_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        last_name = ttk.Entry(form_frame)
        last_name.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Username:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        username = ttk.Entry(form_frame)
        username.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Address:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        address = ttk.Entry(form_frame)
        address.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Birthdate (YYYY-MM-DD):").grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)
        birthdate = ttk.Entry(form_frame)
        birthdate.grid(row=5, column=1, padx=5, pady=5)

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
                    first_name.delete(0, tk.END)
                    last_name.delete(0, tk.END)
                    username.delete(0, tk.END)
                    address.delete(0, tk.END)
                    birthdate.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add owner: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Owner", command=add_owner).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[first_name, last_name, username, address, birthdate])).pack(side=tk.RIGHT, padx=5)

    def add_business_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Business", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Business Name:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        business_name = ttk.Entry(form_frame)
        business_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Rating (1-5):").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        rating = ttk.Entry(form_frame)
        rating.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Spent:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        spent = ttk.Entry(form_frame)
        spent.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Location:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        location = ttk.Entry(form_frame)
        location.grid(row=4, column=1, padx=5, pady=5)

        def add_business():
            if not validate_fields([business_name, rating, spent, location]):
                return
            try:
                r = int(rating.get())
                if r < 1 or r > 5:
                    messagebox.showerror("Validation Error", "Rating must be between 1 and 5.")
                    return
            except ValueError:
                messagebox.showerror("Validation Error", "Rating must be an integer between 1 and 5.")
                return

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
                    business_name.delete(0, tk.END)
                    rating.delete(0, tk.END)
                    spent.delete(0, tk.END)
                    location.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add business: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Business", command=add_business).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[business_name, rating, spent, location])).pack(side=tk.RIGHT, padx=5)

    def add_service_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Service", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Service ID:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        service_id = ttk.Entry(form_frame)
        service_id.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Service Name:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        service_name = ttk.Entry(form_frame)
        service_name.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Home Base:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        home_base = ttk.Entry(form_frame)
        home_base.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Manager Username:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        manager = ttk.Entry(form_frame)
        manager.grid(row=4, column=1, padx=5, pady=5)

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
                    service_id.delete(0, tk.END)
                    service_name.delete(0, tk.END)
                    home_base.delete(0, tk.END)
                    manager.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add service: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Service", command=add_service).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[service_id, service_name, home_base, manager])).pack(side=tk.RIGHT, padx=5)

    def add_location_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Location", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Location Label:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        location_label = ttk.Entry(form_frame)
        location_label.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="X Coordinate:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        x_coord = ttk.Entry(form_frame)
        x_coord.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Y Coordinate:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        y_coord = ttk.Entry(form_frame)
        y_coord.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Space:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        space = ttk.Entry(form_frame)
        space.grid(row=4, column=1, padx=5, pady=5)

        def add_location():
            if not validate_fields([location_label, x_coord, y_coord, space]):
                return
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
                    location_label.delete(0, tk.END)
                    x_coord.delete(0, tk.END)
                    y_coord.delete(0, tk.END)
                    space.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add location: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Location", command=add_location).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[location_label, x_coord, y_coord, space])).pack(side=tk.RIGHT, padx=5)

    def add_employee_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Employee", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Username:", "First Name:", "Last Name:", "Address:", "Birthdate (YYYY-MM-DD):", "Tax ID:", "Hired Date (YYYY-MM-DD):", "Experience (years):", "Salary:"]
        fields = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            fields.append(entry)

        username, first_name, last_name, address, birthdate, tax_id, hired_date, experience, salary = fields

        def add_employee():
            if not validate_fields(fields):
                return
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
                    for field in fields:
                        field.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add employee: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Employee", command=add_employee).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=fields)).pack(side=tk.RIGHT, padx=5)

    def add_driver_role_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Driver Role", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Username:", "License ID:", "License Type:", "Driver Experience (trips):"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        username, license_id, license_type, driver_experience = entries

        def add_driver_role():
            if not validate_fields(entries):
                return
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add driver role: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Driver Role", command=add_driver_role).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def add_worker_role_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Worker Role", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Username:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        username = ttk.Entry(form_frame)
        username.grid(row=1, column=1, padx=5, pady=5)

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
                    username.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add worker role: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Worker Role", command=add_worker_role).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[username])).pack(side=tk.RIGHT, padx=5)

    def add_product_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Product", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Barcode:", "Product Name:", "Weight:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        barcode, product_name, weight = entries

        def add_product():
            if not validate_fields(entries):
                return
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add product: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Product", command=add_product).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[barcode, product_name, weight])).pack(side=tk.RIGHT, padx=5)

    def add_van_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Add Van", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Service ID:", "Tag:", "Fuel:", "Capacity:", "Sales:", "Driven By (Username):"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        service_id, tag, fuel, capacity, sales, driven_by = entries

        def add_van():
            if not validate_fields([service_id, tag, fuel, capacity, sales, driven_by]):
                return
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
                    for field in entries:
                        field.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to add van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add Van", command=add_van).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def start_funding_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Start Funding", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Owner Username:", "Amount:", "Business Name:", "Fund Date (YYYY-MM-DD):"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        owner_username, amount, business_name, fund_date = entries

        def start_funding():
            if not validate_fields(entries):
                return
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to start funding: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Start Funding", command=start_funding).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def hire_employee_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Hire Employee", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Employee Username:", "Service ID:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        employee_username, service_id = entries

        def hire_employee():
            if not validate_fields(entries):
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to hire employee: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Hire Employee", command=hire_employee).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def fire_employee_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Fire Employee", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Employee Username:", "Service ID:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        employee_username, service_id = entries

        def fire_employee():
            if not validate_fields(entries):
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to fire employee: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Fire Employee", command=fire_employee).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def manage_service_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Manage Service", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Employee Username:", "Service ID:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        employee_username, service_id = entries

        def manage_service():
            if not validate_fields(entries):
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to manage service: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Manage Service", command=manage_service).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def takeover_van_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Takeover Van", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Driver Username:", "Service ID:", "Van Tag:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        driver_username, service_id, van_tag = entries

        def takeover_van():
            if not validate_fields(entries):
                return
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to takeover van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Takeover Van", command=takeover_van).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def load_van_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Load Van", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Service ID:", "Van Tag:", "Product Barcode:", "More Packages:", "Price:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        service_id, van_tag, product_barcode, more_packages, price = entries

        def load_van():
            if not validate_fields(entries):
                return
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to load van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Load Van", command=load_van).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def refuel_van_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Refuel Van", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Service ID:", "Van Tag:", "More Fuel:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        service_id, van_tag, more_fuel = entries

        def refuel_van():
            if not validate_fields(entries):
                return
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to refuel van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Refuel Van", command=refuel_van).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def drive_van_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Drive Van", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Service ID:", "Van Tag:", "Destination Location:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        service_id, van_tag, destination = entries

        def drive_van():
            if not validate_fields(entries):
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to drive van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Drive Van", command=drive_van).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def purchase_product_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Purchase Product", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Business Name:", "Service ID:", "Van Tag:", "Product Barcode:", "Quantity:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        business_name, service_id, van_tag, product_barcode, quantity = entries

        def purchase_product():
            if not validate_fields(entries):
                return
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
                    for e in entries:
                        e.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to purchase product: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Purchase Product", command=purchase_product).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def remove_product_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Remove Product", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Product Barcode:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        product_barcode = ttk.Entry(form_frame)
        product_barcode.grid(row=1, column=1, padx=5, pady=5)

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
                    product_barcode.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to remove product: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Remove Product", command=remove_product).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[product_barcode])).pack(side=tk.RIGHT, padx=5)

    def remove_van_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Remove Van", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        labels = ["Service ID:", "Van Tag:"]
        entries = []
        for i, lbl in enumerate(labels, start=1):
            ttk.Label(form_frame, text=lbl).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            e = ttk.Entry(form_frame)
            e.grid(row=i, column=1, padx=5, pady=5)
            entries.append(e)

        service_id, van_tag = entries

        def remove_van():
            if not validate_fields([service_id, van_tag]):
                return
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
                    service_id.delete(0, tk.END)
                    van_tag.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to remove van: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Remove Van", command=remove_van).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=entries)).pack(side=tk.RIGHT, padx=5)

    def remove_driver_role_form(self):
        form_frame = ttk.Frame(self.right_frame, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Remove Driver Role", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(form_frame, text="Driver Username:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        driver_username = ttk.Entry(form_frame)
        driver_username.grid(row=1, column=1, padx=5, pady=5)

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
                    driver_username.delete(0, tk.END)
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to remove driver role: {err}")
                    print(f"Stored procedure error: {err}")
                finally:
                    close_db(conn)

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Remove Driver Role", command=remove_driver_role).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.clear_fields(fields=[driver_username])).pack(side=tk.RIGHT, padx=5)

    # -------------------- View Display Methods --------------------
    def display_owner_view(self):
        display_frame = ttk.Frame(self.right_frame, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(display_frame, text="Owner View", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("Username", "First Name", "Last Name", "Address",
                                               "Businesses Funded", "Locations", "Highest Rating",
                                               "Lowest Rating", "Total Debt"), show='headings')

        headings = [
            ("Username", "Username"),
            ("First Name", "First Name"),
            ("Last Name", "Last Name"),
            ("Address", "Address"),
            ("Businesses Funded", "num_businesses"),
            ("Locations", "num_locations"),
            ("Highest Rating", "max_rating"),
            ("Lowest Rating", "min_rating"),
            ("Total Debt", "total_debt")
        ]
        for col, text in headings:
            tree.heading(col, text=text)
            tree.column(col, anchor=tk.CENTER, width=120)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        def load_owner_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM display_owner_view")
                    rows = cursor.fetchall()
                    for item in tree.get_children():
                        tree.delete(item)
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("username"),
                            row.get("first_name"),
                            row.get("last_name"),
                            row.get("address"),
                            row.get("num_businesses"),
                            row.get("num_places"),  # Adjusted to match the new column name 'num_places'
                            row.get("highs"),       # Adjusted to match column 'highs'
                            row.get("lows"),        # Adjusted to match column 'lows'
                            row.get("debt")         # Adjusted to match column 'debt'
                        ))
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to load owner view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        load_button = ttk.Button(display_frame, text="Load View", command=load_owner_view)
        load_button.pack(pady=10, anchor='e')

    def display_employee_view(self):
        display_frame = ttk.Frame(self.right_frame, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(display_frame, text="Employee View", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("Username", "Tax ID", "Salary", "Hired Date", "Experience",
                                               "License ID", "Driver Experience", "Is Manager"), show='headings')

        headings = [
            ("Username", "Username"),
            ("Tax ID", "taxID"),
            ("Salary", "Salary"),
            ("Hired Date", "hiring_date"),
            ("Experience", "experience_level"),
            ("License ID", "license_identifier"),
            ("Driver Experience", "driving_experience"),
            ("Is Manager", "manager_status")
        ]
        for col, text in headings:
            tree.heading(col, text=text)
            tree.column(col, anchor=tk.CENTER, width=100)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        def load_employee_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM display_employee_view")
                    rows = cursor.fetchall()
                    for item in tree.get_children():
                        tree.delete(item)
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("username"),
                            row.get("taxID"),
                            row.get("salary"),
                            row.get("hired"),
                            row.get("employee_experience"),
                            row.get("if(d.licenseID is null, 'n/a', d.licenseID)") if "if(d.licenseID is null, 'n/a', d.licenseID)" in row else row.get("licenseID"),
                            row.get("driving_experience"),
                            row.get("manager_status")
                        ))
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to load employee view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        load_button = ttk.Button(display_frame, text="Load View", command=load_employee_view)
        load_button.pack(pady=10, anchor='e')

    def display_driver_view(self):
        display_frame = ttk.Frame(self.right_frame, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(display_frame, text="Driver View", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("Username", "License ID", "Driving Experience", "Vans Controlled"), show='headings')

        headings = [
            ("Username", "Username"),
            ("License ID", "License ID"),
            ("Driving Experience", "driving_experience"),
            ("Vans Controlled", "num_vans")
        ]
        for col, text in headings:
            tree.heading(col, text=text)
            tree.column(col, anchor=tk.CENTER, width=150)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        def load_driver_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM display_driver_view")
                    rows = cursor.fetchall()
                    for item in tree.get_children():
                        tree.delete(item)
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("username"),
                            row.get("licenseID"),
                            row.get("successful_trips"),
                            row.get("num_vans")
                        ))
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to load driver view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        load_button = ttk.Button(display_frame, text="Load View", command=load_driver_view)
        load_button.pack(pady=10, anchor='e')

    def display_location_view(self):
        display_frame = ttk.Frame(self.right_frame, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(display_frame, text="Location View", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("Label", "X Coord", "Y Coord", "Long Name",
                                               "Number of Vans", "Van IDs", "Capacity", "Remaining Capacity"), show='headings')

        headings = [
            ("Label", "label"),
            ("X Coord", "x_coord"),
            ("Y Coord", "y_coord"),
            ("Long Name", "long_name"),
            ("Number of Vans", "count(v.located_at)"),
            ("Van IDs", "van_identifiers"),
            ("Capacity", "space"),
            ("Remaining Capacity", "remaining_capacity")
        ]
        for col, text in headings:
            tree.heading(col, text=text)
            tree.column(col, anchor=tk.CENTER, width=120)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        def load_location_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM display_location_view")
                    rows = cursor.fetchall()
                    for item in tree.get_children():
                        tree.delete(item)
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("label"),
                            row.get("x_coord"),
                            row.get("y_coord"),
                            row.get("long_name"),
                            row.get("count(v.located_at)"),
                            row.get("van_identifiers"),
                            row.get("space"),
                            row.get("remaining_capacity")
                        ))
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to load location view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        load_button = ttk.Button(display_frame, text="Load View", command=load_location_view)
        load_button.pack(pady=10, anchor='e')

    def display_product_view(self):
        display_frame = ttk.Frame(self.right_frame, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(display_frame, text="Product View", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("Product Name", "Location", "Amount Available", "Low Price", "High Price"), show='headings')

        headings = [
            ("Product Name", "product_name"),
            ("Location", "location"),
            ("Amount Available", "amount_available"),
            ("Low Price", "low_price"),
            ("High Price", "high_price")
        ]
        for col, text in headings:
            tree.heading(col, text=text)
            tree.column(col, anchor=tk.CENTER, width=120)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        def load_product_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM display_product_view")
                    rows = cursor.fetchall()
                    for item in tree.get_children():
                        tree.delete(item)
                    for row in rows:
                        tree.insert("", tk.END, values=(
                            row.get("product_name"),
                            row.get("location"),
                            row.get("amount_available"),
                            row.get("low_price"),
                            row.get("high_price")
                        ))
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to load product view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        load_button = ttk.Button(display_frame, text="Load View", command=load_product_view)
        load_button.pack(pady=10, anchor='e')

    def display_service_view(self):
        display_frame = ttk.Frame(self.right_frame, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(display_frame, text="Service View", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=("Service ID", "Service Name", "Home Base", "Manager",
                                               "Revenue", "Products Carried", "Cost Carried", "Weight Carried"), show='headings')
        headings = [
            ("Service ID", "id"),
            ("Service Name", "long_name"),
            ("Home Base", "home_base"),
            ("Manager", "manager"),
            ("Revenue", "revenue"),
            ("Products Carried", "products_carried"),
            ("Cost Carried", "cost_carried"),
            ("Weight Carried", "weight_carried")
        ]
        for col, text in headings:
            tree.heading(col, text=text)
            tree.column(col, anchor=tk.CENTER, width=120)

        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        def load_service_view():
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT * FROM display_service_view")
                    rows = cursor.fetchall()
                    for item in tree.get_children():
                        tree.delete(item)
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
                except pymysql.MySQLError as err:
                    messagebox.showerror("Error", f"Failed to load service view: {err}")
                    print(f"View load error: {err}")
                finally:
                    close_db(conn)

        load_button = ttk.Button(display_frame, text="Load View", command=load_service_view)
        load_button.pack(pady=10, anchor='e')

    # -------------------- NEW: Display Table Method --------------------
    def display_table(self, table_name):
        display_frame = ttk.Frame(self.right_frame, padding=10)
        display_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(display_frame, text=f"Table: {table_name}", font=("Helvetica", 16)).pack(pady=10)

        tree_frame = ttk.Frame(display_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Dynamically get columns
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"SHOW COLUMNS FROM {table_name}")
                columns_info = cursor.fetchall()
                columns = [col["Field"] for col in columns_info]

                tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, anchor=tk.CENTER, width=120)

                vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
                hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
                tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

                tree.grid(row=0, column=0, sticky='nsew')
                vsb.grid(row=0, column=1, sticky='ns')
                hsb.grid(row=1, column=0, sticky='ew')

                tree_frame.rowconfigure(0, weight=1)
                tree_frame.columnconfigure(0, weight=1)

                def load_table():
                    c = connect_db()
                    if c:
                        cur = c.cursor()
                        try:
                            cur.execute(f"SELECT * FROM {table_name}")
                            rows = cur.fetchall()
                            for item in tree.get_children():
                                tree.delete(item)
                            for row in rows:
                                values = [row.get(col) for col in columns]
                                tree.insert("", tk.END, values=values)
                        except pymysql.MySQLError as err:
                            messagebox.showerror("Error", f"Failed to load table {table_name}: {err}")
                            print(f"Table load error: {err}")
                        finally:
                            close_db(c)

                load_button = ttk.Button(display_frame, text="Load Table", command=load_table)
                load_button.pack(pady=10, anchor='e')

            except pymysql.MySQLError as err:
                messagebox.showerror("Error", f"Failed to retrieve columns for {table_name}: {err}")
                print(f"Table column fetch error: {err}")
            finally:
                close_db(conn)

    def clear_fields(self, fields):
        for field in fields:
            field.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessSupplyApp(root)
    root.mainloop()