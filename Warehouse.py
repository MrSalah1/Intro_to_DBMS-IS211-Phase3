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
        self.root.title("Smart Warehousing & Inventory System - Phase 2")
        self.root.geometry("1250x650")  # Expanded to fit the new store items panel

        # Check connection status
        if not db.connected:
            messagebox.showerror("Database Error", f"Could not connect to SQL Server:\n{db.error}")
            root.destroy()
            return

        self.setup_ui()

    def setup_ui(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="Smart Warehousing Management", font=("Helvetica", 16, "bold"), fg="white",
                 bg="#2c3e50").pack()

        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(fill=tk.X, padx=10)

        fac_frame = tk.LabelFrame(control_frame, text="1. Facility Management", padx=10, pady=10)
        fac_frame.grid(row=0, column=0, padx=10, sticky=tk.N)

        tk.Label(fac_frame, text="Facility ID:").grid(row=0, column=0, sticky=tk.W)
        self.fac_id_entry = tk.Entry(fac_frame)
        self.fac_id_entry.grid(row=0, column=1, pady=2)

        tk.Label(fac_frame, text="Zone:").grid(row=1, column=0, sticky=tk.W)
        self.fac_zone_entry = tk.Entry(fac_frame)
        self.fac_zone_entry.grid(row=1, column=1, pady=2)

        tk.Label(fac_frame, text="Climate (Yes/No):").grid(row=2, column=0, sticky=tk.W)
        self.fac_climate_entry = tk.Entry(fac_frame)
        self.fac_climate_entry.grid(row=2, column=1, pady=2)

        tk.Button(fac_frame, text="Insert Facility", command=self.insert_facility).grid(row=3, column=0, pady=5,
                                                                                        sticky=tk.EW)
        tk.Button(fac_frame, text="Update Climate", command=self.update_facility).grid(row=3, column=1, pady=5,
                                                                                       sticky=tk.EW)
        tk.Button(fac_frame, text="Delete Facility", command=self.delete_facility).grid(row=4, column=0, columnspan=2,
                                                                                        pady=5, sticky=tk.EW)

        cli_frame = tk.LabelFrame(control_frame, text="2. Client Management", padx=10, pady=10)
        cli_frame.grid(row=0, column=1, padx=10, sticky=tk.N)

        tk.Label(cli_frame, text="Client ID:").grid(row=0, column=0, sticky=tk.W)
        self.cli_id_entry = tk.Entry(cli_frame)
        self.cli_id_entry.grid(row=0, column=1, pady=2)

        tk.Label(cli_frame, text="Client Name:").grid(row=1, column=0, sticky=tk.W)
        self.cli_name_entry = tk.Entry(cli_frame)
        self.cli_name_entry.grid(row=1, column=1, pady=2)

        tk.Button(cli_frame, text="Insert Client", command=self.insert_client).grid(row=2, column=0, pady=5,
                                                                                    sticky=tk.EW)
        tk.Button(cli_frame, text="Update Name", command=self.update_client).grid(row=2, column=1, pady=5, sticky=tk.EW)
        tk.Button(cli_frame, text="Delete Client", command=self.delete_client).grid(row=3, column=0, columnspan=2,
                                                                                    pady=5, sticky=tk.EW)

        store_frame = tk.LabelFrame(control_frame, text="3. Store Items", padx=10, pady=10)
        store_frame.grid(row=0, column=2, padx=10, sticky=tk.N)

        tk.Label(store_frame, text="Agreement ID:").grid(row=0, column=0, sticky=tk.W)
        self.agr_id_entry = tk.Entry(store_frame, width=15)
        self.agr_id_entry.grid(row=0, column=1, pady=2)

        tk.Label(store_frame, text="Client ID:").grid(row=1, column=0, sticky=tk.W)
        self.agr_cli_entry = tk.Entry(store_frame, width=15)
        self.agr_cli_entry.grid(row=1, column=1, pady=2)

        tk.Label(store_frame, text="Facility ID:").grid(row=2, column=0, sticky=tk.W)
        self.agr_fac_entry = tk.Entry(store_frame, width=15)
        self.agr_fac_entry.grid(row=2, column=1, pady=2)

        tk.Label(store_frame, text="Product ID:").grid(row=3, column=0, sticky=tk.W)
        self.agr_prod_entry = tk.Entry(store_frame, width=15)
        self.agr_prod_entry.grid(row=3, column=1, pady=2)

        tk.Label(store_frame, text="Quantity:").grid(row=4, column=0, sticky=tk.W)
        self.agr_qty_entry = tk.Entry(store_frame, width=15)
        self.agr_qty_entry.grid(row=4, column=1, pady=2)

        tk.Button(store_frame, text="Create Agreement & Store", command=self.insert_stored_items).grid(row=5, column=0,
                                                                                                       columnspan=2,
                                                                                                       pady=5,
                                                                                                       sticky=tk.EW)


        view_frame = tk.LabelFrame(control_frame, text="4. Data Views", padx=10, pady=10)
        view_frame.grid(row=0, column=3, padx=10, sticky=tk.N)

        tk.Button(view_frame, text="Simple Select (All Facilities)", width=35, command=self.view_facilities).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  pady=5)
        tk.Button(view_frame, text="Complex Select (Client Totals with JOIN)", width=35,
                  command=self.view_client_totals).grid(row=1, column=0, pady=5)
        tk.Button(view_frame, text="Clear Grid", width=35, command=self.clear_grid).grid(row=2, column=0, pady=5)


        grid_frame = tk.Frame(self.root, padx=10, pady=10)
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
        """Helper to wipe the grid"""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = []

    def display_results(self, columns, rows):
        """Helper to insert new data into the Treeview"""
        self.clear_grid()
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=tk.CENTER)

        for row in rows:
            clean_row = [str(item) if item is not None else "0" for item in row]
            self.tree.insert("", tk.END, values=clean_row)


    def insert_facility(self):
        fid = self.fac_id_entry.get()
        zone = self.fac_zone_entry.get()
        climate = self.fac_climate_entry.get()

        if not fid or not zone or not climate:
            messagebox.showwarning("Input Error", "Please fill Facility ID, Zone, and Climate.")
            return

        try:
            self.db.execute_action("INSERT INTO FACILITY (FACILITY_ID, ZONE, CLIMATE_CONTROL) VALUES (?, ?, ?)",
                                   (fid, zone, climate))
            messagebox.showinfo("Success", f"Inserted Facility {fid} successfully!")
            self.view_facilities()  # Auto refresh the grid
        except Exception as e:
            messagebox.showerror("Insert Error", str(e))

    def update_facility(self):
        fid = self.fac_id_entry.get()
        climate = self.fac_climate_entry.get()

        if not fid or not climate:
            messagebox.showwarning("Input Error", "Please provide a Facility ID and the new Climate value.")
            return

        try:
            self.db.execute_action("UPDATE FACILITY SET CLIMATE_CONTROL = ? WHERE FACILITY_ID = ?", (climate, fid))
            messagebox.showinfo("Success", f"Updated Facility {fid} climate to '{climate}'.")
            self.view_facilities()
        except Exception as e:
            messagebox.showerror("Update Error", str(e))

    def delete_facility(self):
        fid = self.fac_id_entry.get()

        if not fid:
            messagebox.showwarning("Input Error", "Please provide a Facility ID to delete.")
            return

        try:
            self.db.execute_action("DELETE FROM FACILITY WHERE FACILITY_ID = ?", (fid,))
            messagebox.showinfo("Success", f"Deleted Facility {fid}.")
            self.view_facilities()
        except Exception as e:
            messagebox.showerror("Delete Error",
                                 f"Cannot delete Facility {fid} (Check if it has linked sections!)\n\nDetails: {str(e)}")

    def insert_client(self):
        cid = self.cli_id_entry.get()
        cname = self.cli_name_entry.get()

        if not cid or not cname:
            messagebox.showwarning("Input Error", "Please fill Client ID and Client Name.")
            return

        try:
            self.db.execute_action("INSERT INTO CLIENT (CLIENT_ID, CLIENT_NAME) VALUES (?, ?)", (cid, cname))
            messagebox.showinfo("Success", f"Inserted Client '{cname}' successfully!")
            self.view_client_totals()
        except Exception as e:
            messagebox.showerror("Insert Error", str(e))

    def update_client(self):
        cid = self.cli_id_entry.get()
        cname = self.cli_name_entry.get()

        if not cid or not cname:
            messagebox.showwarning("Input Error", "Please provide a Client ID and the new Client Name.")
            return

        try:
            self.db.execute_action("UPDATE CLIENT SET CLIENT_NAME = ? WHERE CLIENT_ID = ?", (cname, cid))
            messagebox.showinfo("Success", f"Updated Client {cid} name to '{cname}'.")
            self.view_client_totals()
        except Exception as e:
            messagebox.showerror("Update Error", str(e))

    def delete_client(self):
        cid = self.cli_id_entry.get()

        if not cid:
            messagebox.showwarning("Input Error", "Please provide a Client ID to delete.")
            return

        try:
            self.db.execute_action("DELETE FROM CLIENT WHERE CLIENT_ID = ?", (cid,))
            messagebox.showinfo("Success", f"Deleted Client {cid}.")
            self.view_client_totals()
        except Exception as e:
            messagebox.showerror("Delete Error",
                                 f"Cannot delete Client {cid} (Check if they have active storage agreements!)\n\nDetails: {str(e)}")

    def insert_stored_items(self):
        agr_id = self.agr_id_entry.get()
        cli_id = self.agr_cli_entry.get()
        fac_id = self.agr_fac_entry.get()
        prod_id = self.agr_prod_entry.get()
        qty = self.agr_qty_entry.get()

        if not all([agr_id, cli_id, fac_id, prod_id, qty]):
            messagebox.showwarning("Input Error", "Please fill all fields to store items.")
            return

        try:

            query1 = "INSERT INTO STORAGE_AGREEMENT (AGREEMENT_ID, CLIENT_ID, FACILITY_ID, AGREEMENT_DATE) VALUES (?, ?, ?, CURRENT_TIMESTAMP)"
            self.db.execute_action(query1, (agr_id, cli_id, fac_id))

            query2 = "INSERT INTO INCLUDES (AGREEMENT_ID, PRODUCT_ID, QUANTITY_STORED) VALUES (?, ?, ?)"
            self.db.execute_action(query2, (agr_id, prod_id, qty))

            messagebox.showinfo("Success", f"Stored {qty} units of Product {prod_id} under Agreement {agr_id}!")
            self.view_client_totals()
        except Exception as e:
            messagebox.showerror("Insert Error",
                                 f"Failed to store items.\nMake sure Client, Facility, and Product IDs actually exist in their tables first!\n\nDetails: {str(e)}")

    def view_facilities(self):
        try:
            query = "SELECT * FROM FACILITY"
            cols, rows = self.db.fetch_data(query)
            self.display_results(cols, rows)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))

    def view_client_totals(self):
        try:
            query = """
            SELECT 
                C.CLIENT_ID, 
                C.CLIENT_NAME, 
                SUM(I.QUANTITY_STORED) AS TOTAL_STORED_ITEMS
            FROM 
                CLIENT C
            LEFT JOIN 
                STORAGE_AGREEMENT SA ON C.CLIENT_ID = SA.CLIENT_ID
            LEFT JOIN 
                INCLUDES I ON SA.AGREEMENT_ID = I.AGREEMENT_ID
            GROUP BY 
                C.CLIENT_ID, C.CLIENT_NAME
            """
            cols, rows = self.db.fetch_data(query)
            self.display_results(cols, rows)
        except Exception as e:
            messagebox.showerror("Query Error", str(e))


if __name__ == "__main__":

    root = tk.Tk()


    database = WarehouseDatabase()


    app = WarehouseApp(root, database)


    root.mainloop()

    database.close()