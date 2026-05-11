import pyodbc
import sys


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


class WarehouseCLI:
    def __init__(self, db):
        self.db = db
        if not self.db.connected:
            print(f"\n[!] Database Connection Failed: {self.db.error}")
            sys.exit(1)

    # -----------------------------------------
    # Helper: Print Data as a Text Table
    # -----------------------------------------
    def print_table(self, columns, rows):
        if not rows:
            print("\n[ No records found. ]\n")
            return

        # Calculate column widths
        col_widths = [len(col) for col in columns]
        clean_rows = []
        for row in rows:
            clean_row = [str(item) if item is not None else "0" for item in row]
            clean_rows.append(clean_row)
            for i, item in enumerate(clean_row):
                if len(item) > col_widths[i]:
                    col_widths[i] = len(item)

        # Print Headers
        print("\n" + "-" * (sum(col_widths) + len(columns) * 3 + 1))
        header = "| " + " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns)) + " |"
        print(header)
        print("-" * (sum(col_widths) + len(columns) * 3 + 1))

        # Print Rows
        for row in clean_rows:
            row_str = "| " + " | ".join(item.ljust(col_widths[i]) for i, item in enumerate(row)) + " |"
            print(row_str)
        print("-" * (sum(col_widths) + len(columns) * 3 + 1) + "\n")

    def run_query(self, query):
        try:
            cols, rows = self.db.fetch_data(query)
            self.print_table(cols, rows)
        except Exception as e:
            print(f"\n[!] Query Error: {e}\n")

    # -----------------------------------------
    # Menus
    # -----------------------------------------
    def main_menu(self):
        while True:
            print("========================================")
            print("  SMART WAREHOUSE SYSTEM (CLI MODE)")
            print("========================================")
            print("1. Admin / Setup")
            print("2. Daily Operations")
            print("3. Inquiries & Reports")
            print("4. Exit")

            choice = input("Select an option (1-4): ")

            if choice == '1':
                self.admin_menu()
            elif choice == '2':
                self.ops_menu()
            elif choice == '3':
                self.reports_menu()
            elif choice == '4':
                print("Exiting system...")
                break
            else:
                print("Invalid choice. Please try again.\n")

    def admin_menu(self):
        print("\n--- Admin / Setup ---")
        print("1. Register Facility")
        print("2. Register Section")
        print("3. Register Client")
        print("4. Register Employee")
        print("5. Register Industry Group")
        print("6. Register Manufacturer")
        print("0. Back to Main Menu")

        choice = input("Select operation: ")

        try:
            if choice == '1':
                data = [input("Facility ID: "), input("Zone: "), input("Climate (Yes/No): ")]
                self.db.execute_action("INSERT INTO FACILITY VALUES (?, ?, ?)", data)
                print("[+] Facility Inserted Successfully!\n")

            elif choice == '2':
                data = [input("Section ID: "), input("Facility ID: "), input("Section Code: ")]
                self.db.execute_action("INSERT INTO SECTION VALUES (?, ?, ?)", data)
                print("[+] Section Inserted Successfully!\n")

            elif choice == '3':
                data = [input("Client ID: "), input("Client Name: ")]
                self.db.execute_action("INSERT INTO CLIENT VALUES (?, ?)", data)
                print("[+] Client Inserted Successfully!\n")

            elif choice == '4':
                data = [input("Employee ID: "), input("Name: ")]
                self.db.execute_action("INSERT INTO EMPLOYEE VALUES (?, ?)", data)
                print("[+] Employee Inserted Successfully!\n")

            elif choice == '5':
                data = [input("Group ID: "), input("Group Name: ")]
                self.db.execute_action("INSERT INTO INDUSTRY_GROUP VALUES (?, ?)", data)
                print("[+] Industry Group Inserted Successfully!\n")

            elif choice == '6':
                data = [input("Manufacturer ID: "), input("Manufacturer Name: ")]
                self.db.execute_action("INSERT INTO MANUFACTURER VALUES (?, ?)", data)
                print("[+] Manufacturer Inserted Successfully!\n")

        except Exception as e:
            print(f"\n[!] Insert Error: {e}\n")

    def ops_menu(self):
        print("\n--- Daily Operations ---")
        print("1. Catalog Product")
        print("2. Create Storage Agreement")
        print("3. Log Inventory Movement")
        print("0. Back to Main Menu")

        choice = input("Select operation: ")

        try:
            if choice == '1':
                data = [input("Product ID: "), input("Group ID: "), input("Manufacturer ID: "),
                        input("Dimensions: "), input("Weight: "), input("Product Name: ")]
                self.db.execute_action("INSERT INTO PRODUCT VALUES (?, ?, ?, ?, ?, ?)", data)
                print("[+] Product Cataloged Successfully!\n")

            elif choice == '2':
                agr_id = input("Agreement ID: ")
                cli_id = input("Client ID: ")
                fac_id = input("Facility ID: ")
                prod_id = input("Product ID: ")
                qty = input("Quantity: ")

                self.db.execute_action(
                    "INSERT INTO STORAGE_AGREEMENT (AGREEMENT_ID, CLIENT_ID, FACILITY_ID, AGREEMENT_DATE) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                    [agr_id, cli_id, fac_id])
                self.db.execute_action(
                    "INSERT INTO INCLUDES (AGREEMENT_ID, PRODUCT_ID, QUANTITY_STORED) VALUES (?, ?, ?)",
                    [agr_id, prod_id, qty])
                print("[+] Agreement created and item stored successfully!\n")

            elif choice == '3':
                data = [input("Movement ID: "), input("Product ID: "), input("Source Section ID: "),
                        input("Dest Section ID: "), input("Employee ID: ")]
                self.db.execute_action(
                    "INSERT INTO INVENTORY_MOVEMENT (MOVEMENT_ID, PRODUCT_ID, SECTION_ID, SEC_SECTION_ID, EMPLOYEE_ID, MOVEMENT_TIMESTAMP) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                    data)
                print("[+] Movement Logged Successfully!\n")

        except Exception as e:
            print(f"\n[!] Insert Error: {e}\n")

    def reports_menu(self):
        print("\n--- Inquiries & Reports ---")
        print("1. Max Industry Group Agreements (Last Month)")
        print("2. Products With No Storage/Movement (Last Month)")
        print("3. Staff with Max Inventory Movements (Last Month)")
        print("4. Manufacturers with No Products Stored (Last Month)")
        print("5. Specific Products Stored at Each Facility (Last Month)")
        print("6. Full Client Details & Total Items Stored")
        print("7. Facility Capacity & Distribution by Industry (Bonus)")
        print("0. Back to Main Menu")

        choice = input("Select report: ")

        if choice == '1':
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

        elif choice == '2':
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

        elif choice == '3':
            query = """
            SELECT TOP 1 E.EMPLOYEE_ID, E.EMPLOYEE_NAME, COUNT(IM.MOVEMENT_ID) AS MoveCount
            FROM EMPLOYEE E
            JOIN INVENTORY_MOVEMENT IM ON E.EMPLOYEE_ID = IM.EMPLOYEE_ID
            WHERE DATEDIFF(month, IM.MOVEMENT_TIMESTAMP, GETDATE()) = 1
            GROUP BY E.EMPLOYEE_ID, E.EMPLOYEE_NAME
            ORDER BY MoveCount DESC
            """
            self.run_query(query)

        elif choice == '4':
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

        elif choice == '5':
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

        elif choice == '6':
            query = """
            SELECT C.CLIENT_ID, C.CLIENT_NAME, ISNULL(SUM(I.QUANTITY_STORED), 0) AS TotalItemsStored
            FROM CLIENT C
            LEFT JOIN STORAGE_AGREEMENT SA ON C.CLIENT_ID = SA.CLIENT_ID
            LEFT JOIN INCLUDES I ON SA.AGREEMENT_ID = I.AGREEMENT_ID
            GROUP BY C.CLIENT_ID, C.CLIENT_NAME
            ORDER BY TotalItemsStored DESC
            """
            self.run_query(query)

        elif choice == '7':
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
    db = WarehouseDatabase()
    cli = WarehouseCLI(db)

    try:
        cli.main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram forcibly interrupted. Exiting safely...")
    finally:
        db.close()