import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox


class WarehouseDatabase:
    def __init__(self):
        self.conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=localhost;'
            r'DATABASE=SmartWarehouse;'
            r'Trusted_Connection=yes;'
        )
        try:
            self.conn = pyodbc.connect(self.conn_str)
            self.cursor = self.conn.cursor()
            self.connected = True
        except Exception as e:
            self.connected = False
            self.error = str(e)

    def execute_action(self, query, params=()):
        """Used for INSERT, UPDATE, DELETE"""
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_data(self, query, params=()):
        """Used for SELECT queries. Returns column names and rows."""
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        columns = [column[0] for column in self.cursor.description]
        return columns, rows

    def close(self):
        if self.connected:
            self.cursor.close()
            self.conn.close()


class WarehouseApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Smart Warehousing & Inventory System - Full System")
        self.root.geometry("1250x750")

        if not db.connected:
            messagebox.showerror("Database Error", f"Could not connect to SQL Server:\n{db.error}")
            root.destroy()
            return

        self.setup_ui()

    def create_form(self, parent, title, fields, row_offset, col_offset):
        """Helper to create entry forms quickly"""
        frame = tk.LabelFrame(parent, text=title, padx=10, pady=10)
        frame.grid(row=row_offset, column=col_offset, padx=10, pady=5, sticky=tk.N + tk.EW)
        entries = {}
        for i, field in enumerate(fields):
            tk.Label(frame, text=field + ":").grid(row=i, column=0, sticky=tk.W, pady=2)
            ent = tk.Entry(frame, width=20)
            ent.grid(row=i, column=1, pady=2, padx=5, sticky=tk.E)
            entries[field] = ent
        return frame, entries

    def setup_ui(self):
        # Top Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Smart Warehousing & Inventory Management", font=("Helvetica", 16, "bold"),
                 fg="white", bg="#2c3e50").pack()

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.X, padx=10, pady=10)

        tab_admin = ttk.Frame(self.notebook)
        tab_ops = ttk.Frame(self.notebook)
        tab_reports = ttk.Frame(self.notebook)

        self.notebook.add(tab_admin, text="1. Admin / Setup")
        self.notebook.add(tab_ops, text="2. Daily Operations")
        self.notebook.add(tab_reports, text="3. Inquiries & Reports")

        # ==========================================
        # TAB 1: ADMIN & SETUP (Facilities, Sections, Clients, Staff, Manufacturers)
        # ==========================================
        # Facility & Section
        fac_frame, self.fac_entries = self.create_form(tab_admin, "Register Facility",
                                                       ["Facility ID", "Zone", "Climate"], 0, 0)
        tk.Button(fac_frame, text="Insert Facility", command=self.insert_facility).grid(row=3, column=0, columnspan=2,
                                                                                        pady=5, sticky=tk.EW)

        sec_frame, self.sec_entries = self.create_form(tab_admin, "Register Section",
                                                       ["Section ID", "Facility ID", "Section Code"], 1, 0)
        tk.Button(sec_frame, text="Insert Section", command=self.insert_section).grid(row=3, column=0, columnspan=2,
                                                                                      pady=5, sticky=tk.EW)

        # Clients & Staff
        cli_frame, self.cli_entries = self.create_form(tab_admin, "Register Client", ["Client ID", "Client Name"], 0, 1)
        tk.Button(cli_frame, text="Insert Client", command=self.insert_client).grid(row=2, column=0, columnspan=2,
                                                                                    pady=5, sticky=tk.EW)

        emp_frame, self.emp_entries = self.create_form(tab_admin, "Register Employee", ["Employee ID", "Name"], 1, 1)
        tk.Button(emp_frame, text="Insert Employee", command=self.insert_employee).grid(row=2, column=0, columnspan=2,
                                                                                        pady=5, sticky=tk.EW)

        # Industry & Manufacturer
        ind_frame, self.ind_entries = self.create_form(tab_admin, "Register Industry Group", ["Group ID", "Group Name"],
                                                       0, 2)
        tk.Button(ind_frame, text="Insert Industry", command=self.insert_industry).grid(row=2, column=0, columnspan=2,
                                                                                        pady=5, sticky=tk.EW)

        man_frame, self.man_entries = self.create_form(tab_admin, "Register Manufacturer", ["Manufacturer ID", "Name"],
                                                       1, 2)
        tk.Button(man_frame, text="Insert Manufacturer", command=self.insert_manufacturer).grid(row=2, column=0,
                                                                                                columnspan=2, pady=5,
                                                                                                sticky=tk.EW)

        # ==========================================
        # TAB 2: DAILY OPERATIONS (Catalog Products, Store Items, Move Inventory)
        # ==========================================
        prod_frame, self.prod_entries = self.create_form(tab_ops, "Catalog Product",
                                                         ["Product ID", "Group ID", "Manufacturer ID", "Dimensions",
                                                          "Weight", "Product Name"], 0, 0)
        tk.Button(prod_frame, text="Catalog Product", command=self.insert_product).grid(row=6, column=0, columnspan=2,
                                                                                        pady=5, sticky=tk.EW)

        agr_frame, self.agr_entries = self.create_form(tab_ops, "Create Storage Agreement",
                                                       ["Agreement ID", "Client ID", "Facility ID", "Product ID",
                                                        "Quantity"], 0, 1)
        tk.Button(agr_frame, text="Create & Store Item", command=self.insert_stored_items).grid(row=5, column=0,
                                                                                                columnspan=2, pady=5,
                                                                                                sticky=tk.EW)

        mov_frame, self.mov_entries = self.create_form(tab_ops, "Log Inventory Movement",
                                                       ["Movement ID", "Product ID", "Source Section ID",
                                                        "Dest Section ID", "Employee ID"], 0, 2)
        tk.Button(mov_frame, text="Log Movement", command=self.insert_movement).grid(row=5, column=0, columnspan=2,
                                                                                     pady=5, sticky=tk.EW)

        # ==========================================
        # TAB 3: INQUIRIES & REPORTS
        # ==========================================
        btn_frame = tk.Frame(tab_reports, pady=10)
        btn_frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(btn_frame, text="1. Max Industry Group Agreements (Last Month)", command=self.inq_1, width=60).grid(
            row=0, column=0, pady=2)
        tk.Button(btn_frame, text="2. Products With No Storage/Movement (Last Month)", command=self.inq_2,
                  width=60).grid(row=1, column=0, pady=2)
        tk.Button(btn_frame, text="3. Staff with Max Inventory Movements (Last Month)", command=self.inq_3,
                  width=60).grid(row=2, column=0, pady=2)
        tk.Button(btn_frame, text="4. Manufacturers with No Products Stored (Last Month)", command=self.inq_4,
                  width=60).grid(row=3, column=0, pady=2)
        tk.Button(btn_frame, text="5. Specific Products Stored at Each Facility (Last Month)", command=self.inq_5,
                  width=60).grid(row=4, column=0, pady=2)
        tk.Button(btn_frame, text="6. Full Client Details & Total Items Stored", command=self.inq_6, width=60).grid(
            row=5, column=0, pady=2)
        tk.Button(btn_frame, text="* Bonus: Facility Capacity & Distribution by Industry", command=self.inq_bonus,
                  width=60).grid(row=6, column=0, pady=2)

        tk.Button(btn_frame, text="Clear Data Grid", command=self.clear_grid, width=30, bg="#e74c3c", fg="white").grid(
            row=7, column=0, pady=10)

        # ==========================================
        # BOTTOM GRID (Always visible)
        # ==========================================
        grid_frame = tk.Frame(self.root, padx=10, pady=5)
        grid_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(grid_frame, text="Query Results / Messages:", font=("Helvetica", 10, "bold")).pack(anchor=tk.W)

        scroll_y = tk.Scrollbar(grid_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = tk.Scrollbar(grid_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(grid_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

    # -----------------------------------------
    # UI HELPER METHODS
    # -----------------------------------------
    def clear_grid(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = []

    def display_results(self, columns, rows):
        self.clear_grid()
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        for row in rows:
            clean_row = [str(item) if item is not None else "0" for item in row]
            self.tree.insert("", tk.END, values=clean_row)

    # -----------------------------------------
    # INSERT METHODS
    # -----------------------------------------
    def insert_facility(self):
        data = [self.fac_entries[k].get() for k in ["Facility ID", "Zone", "Climate"]]
        try:
            self.db.execute_action("INSERT INTO FACILITY (FACILITY_ID, ZONE, CLIMATE_CONTROL) VALUES (?, ?, ?)", data)
            messagebox.showinfo("Success", "Facility Inserted!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_section(self):
        data = [self.sec_entries[k].get() for k in ["Section ID", "Facility ID", "Section Code"]]
        try:
            self.db.execute_action("INSERT INTO SECTION (SECTION_ID, FACILITY_ID, SECTION_CODE) VALUES (?, ?, ?)", data)
            messagebox.showinfo("Success", "Section Inserted!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_client(self):
        data = [self.cli_entries[k].get() for k in ["Client ID", "Client Name"]]
        try:
            self.db.execute_action("INSERT INTO CLIENT (CLIENT_ID, CLIENT_NAME) VALUES (?, ?)", data)
            messagebox.showinfo("Success", "Client Inserted!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_employee(self):
        data = [self.emp_entries[k].get() for k in ["Employee ID", "Name"]]
        try:
            self.db.execute_action("INSERT INTO EMPLOYEE (EMPLOYEE_ID, EMPLOYEE_NAME) VALUES (?, ?)", data)
            messagebox.showinfo("Success", "Employee Inserted!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_industry(self):
        data = [self.ind_entries[k].get() for k in ["Group ID", "Group Name"]]
        try:
            self.db.execute_action("INSERT INTO INDUSTRY_GROUP (GROUP_ID, GROUP_NAME) VALUES (?, ?)", data)
            messagebox.showinfo("Success", "Industry Group Inserted!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_manufacturer(self):
        data = [self.man_entries[k].get() for k in ["Manufacturer ID", "Name"]]
        try:
            self.db.execute_action("INSERT INTO MANUFACTURER (MANUFACTURER_ID, MANUFACTURER_NAME) VALUES (?, ?)", data)
            messagebox.showinfo("Success", "Manufacturer Inserted!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_product(self):
        data = [self.prod_entries[k].get() for k in
                ["Product ID", "Group ID", "Manufacturer ID", "Dimensions", "Weight", "Product Name"]]
        try:
            self.db.execute_action(
                "INSERT INTO PRODUCT (PRODUCT_ID, GROUP_ID, MANUFACTURER_ID, DIMENSIONS, WEIGHT, PRODUCT_NAME) VALUES (?, ?, ?, ?, ?, ?)",
                data)
            messagebox.showinfo("Success", "Product Cataloged!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_movement(self):
        data = [self.mov_entries[k].get() for k in
                ["Movement ID", "Product ID", "Source Section ID", "Dest Section ID", "Employee ID"]]
        try:
            # Timestamp generated by the database
            self.db.execute_action(
                "INSERT INTO INVENTORY_MOVEMENT (MOVEMENT_ID, PRODUCT_ID, SECTION_ID, SEC_SECTION_ID, EMPLOYEE_ID, MOVEMENT_TIMESTAMP) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                data)
            messagebox.showinfo("Success", "Inventory Movement Logged!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def insert_stored_items(self):
        data = [self.agr_entries[k].get() for k in
                ["Agreement ID", "Client ID", "Facility ID", "Product ID", "Quantity"]]
        if not all(data): return messagebox.showwarning("Input Error", "Fill all fields")
        try:
            self.db.execute_action(
                "INSERT INTO STORAGE_AGREEMENT (AGREEMENT_ID, CLIENT_ID, FACILITY_ID, AGREEMENT_DATE) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                data[:3])
            self.db.execute_action("INSERT INTO INCLUDES (AGREEMENT_ID, PRODUCT_ID, QUANTITY_STORED) VALUES (?, ?, ?)",
                                   [data[0], data[3], data[4]])
            messagebox.showinfo("Success", "Agreement created and item stored!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -----------------------------------------
    # INQUIRIES & REPORTS (Functionality 5 & SQL Questions)
    # Note: Using DATEDIFF(month, date, GETDATE()) = 1 to target "last month" strictly.
    # -----------------------------------------
    def run_query(self, query):
        try:
            cols, rows = self.db.fetch_data(query)
            self.display_results(cols, rows)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))

    def inq_1(self):
        # 1. Which industry group had the maximum number of storage agreements last month?
        query = """
        SELECT TOP 1 IG.GROUP_NAME, COUNT(SA.AGREEMENT_ID) as TotalAgreements
        FROM INDUSTRY_GROUP IG
        JOIN PRODUCT P ON IG.GROUP_ID = P.GROUP_ID
        JOIN INCLUDES I ON P.PRODUCT_ID = I.PRODUCT_ID
        JOIN STORAGE_AGREEMENT SA ON I.AGREEMENT_ID = SA.AGREEMENT_ID
        WHERE DATEDIFF(month, SA.AGREEMENT_DATE, GETDATE()) = 1
        GROUP BY IG.GROUP_NAME
        ORDER BY TotalAgreements DESC
        """
        self.run_query(query)

    def inq_2(self):
        # 2. Which specific product had no storage or movement activity recorded last month?
        query = """
        SELECT P.PRODUCT_ID, P.PRODUCT_NAME
        FROM PRODUCT P
        WHERE P.PRODUCT_ID NOT IN (
            SELECT I.PRODUCT_ID FROM INCLUDES I
            JOIN STORAGE_AGREEMENT SA ON I.AGREEMENT_ID = SA.AGREEMENT_ID
            WHERE DATEDIFF(month, SA.AGREEMENT_DATE, GETDATE()) = 1
        )
        AND P.PRODUCT_ID NOT IN (
            SELECT IM.PRODUCT_ID FROM INVENTORY_MOVEMENT IM
            WHERE DATEDIFF(month, IM.MOVEMENT_TIMESTAMP, GETDATE()) = 1
        )
        """
        self.run_query(query)

    def inq_3(self):
        # 3. Who was the staff member who performed the maximum number of inventory movements last month?
        query = """
        SELECT TOP 1 E.EMPLOYEE_ID, E.EMPLOYEE_NAME, COUNT(IM.MOVEMENT_ID) AS MoveCount
        FROM EMPLOYEE E
        JOIN INVENTORY_MOVEMENT IM ON E.EMPLOYEE_ID = IM.EMPLOYEE_ID
        WHERE DATEDIFF(month, IM.MOVEMENT_TIMESTAMP, GETDATE()) = 1
        GROUP BY E.EMPLOYEE_ID, E.EMPLOYEE_NAME
        ORDER BY MoveCount DESC
        """
        self.run_query(query)

    def inq_4(self):
        # 4. Identify manufacturers who did not have any of their products stored in any facility last month?
        query = """
        SELECT M.MANUFACTURER_ID, M.MANUFACTURER_NAME
        FROM MANUFACTURER M
        WHERE M.MANUFACTURER_ID NOT IN (
            SELECT P.MANUFACTURER_ID
            FROM PRODUCT P
            JOIN INCLUDES I ON P.PRODUCT_ID = I.PRODUCT_ID
            JOIN STORAGE_AGREEMENT SA ON I.AGREEMENT_ID = SA.AGREEMENT_ID
            WHERE DATEDIFF(month, SA.AGREEMENT_DATE, GETDATE()) = 1
        )
        """
        self.run_query(query)

    def inq_5(self):
        # 5. What were the specific products stored at each facility last month?
        query = """
        SELECT F.FACILITY_ID, F.ZONE, P.PRODUCT_NAME, SUM(I.QUANTITY_STORED) AS TotalStored
        FROM FACILITY F
        JOIN STORAGE_AGREEMENT SA ON F.FACILITY_ID = SA.FACILITY_ID
        JOIN INCLUDES I ON SA.AGREEMENT_ID = I.AGREEMENT_ID
        JOIN PRODUCT P ON I.PRODUCT_ID = P.PRODUCT_ID
        WHERE DATEDIFF(month, SA.AGREEMENT_DATE, GETDATE()) = 1
        GROUP BY F.FACILITY_ID, F.ZONE, P.PRODUCT_NAME
        ORDER BY F.FACILITY_ID
        """
        self.run_query(query)

    def inq_6(self):
        # 6. For each client, retrieve their full details and the total quantity of items they currently have stored.
        query = """
        SELECT C.CLIENT_ID, C.CLIENT_NAME, ISNULL(SUM(I.QUANTITY_STORED), 0) AS TotalItemsStored
        FROM CLIENT C
        LEFT JOIN STORAGE_AGREEMENT SA ON C.CLIENT_ID = SA.CLIENT_ID
        LEFT JOIN INCLUDES I ON SA.AGREEMENT_ID = I.AGREEMENT_ID
        GROUP BY C.CLIENT_ID, C.CLIENT_NAME
        ORDER BY TotalItemsStored DESC
        """
        self.run_query(query)

    def inq_bonus(self):
        # Additional: Monitoring facility capacity and product distribution by industry group
        query = """
        SELECT F.FACILITY_ID, F.ZONE, IG.GROUP_NAME, SUM(I.QUANTITY_STORED) as TotalItems
        FROM FACILITY F
        JOIN STORAGE_AGREEMENT SA ON F.FACILITY_ID = SA.FACILITY_ID
        JOIN INCLUDES I ON SA.AGREEMENT_ID = I.AGREEMENT_ID
        JOIN PRODUCT P ON I.PRODUCT_ID = P.PRODUCT_ID
        JOIN INDUSTRY_GROUP IG ON P.GROUP_ID = IG.GROUP_ID
        GROUP BY F.FACILITY_ID, F.ZONE, IG.GROUP_NAME
        ORDER BY F.FACILITY_ID
        """
        self.run_query(query)


if __name__ == "__main__":
    root = tk.Tk()
    database = WarehouseDatabase()
    app = WarehouseApp(root, database)
    root.mainloop()
    database.close()