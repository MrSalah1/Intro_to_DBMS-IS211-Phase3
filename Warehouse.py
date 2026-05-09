import pyodbc

class WarehouseDatabase:
    def __init__(self):
        self.conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=localhost;'
            r'DATABASE=SmartWarehouse;'
            r'Trusted_Connection=yes;'
        )
        self.conn = pyodbc.connect(self.conn_str)
        self.cursor = self.conn.cursor()

    # 1. TWO INSERT STATEMENTS
    def insert_facility(self, facility_id, zone, climate_control):
        query = "INSERT INTO FACILITY (FACILITY_ID, ZONE, CLIMATE_CONTROL) VALUES (?, ?, ?)"
        self.cursor.execute(query, (facility_id, zone, climate_control))
        self.conn.commit()
        print(f"Inserted Facility {facility_id} successfully.")

    def insert_client(self, client_id, client_name, contact_info):
        query = "INSERT INTO CLIENT (CLIENT_ID, CLIENT_NAME) VALUES (?, ?)"
        self.cursor.execute(query, (client_id, client_name))
        self.conn.commit()
        print(f"Inserted Client '{client_name}' successfully.")

    # 2. TWO UPDATE STATEMENTS
    def update_facility_climate(self, facility_id, new_climate_status):
        query = "UPDATE FACILITY SET CLIMATE_CONTROL = ? WHERE FACILITY_ID = ?"
        self.cursor.execute(query, (new_climate_status, facility_id))
        self.conn.commit()
        print(f"Updated Facility {facility_id} climate control to '{new_climate_status}'.")

    def update_employee_name(self, employee_id, new_name):
        query = "UPDATE EMPLOYEE SET EMPLOYEE_NAME = ? WHERE EMPLOYEE_ID = ?"
        self.cursor.execute(query, (new_name, employee_id))
        self.conn.commit()
        print(f"Updated Employee {employee_id} name to '{new_name}'.")

    # 3. TWO DELETE STATEMENTS
    def delete_inventory_movement(self, movement_id):
        query = "DELETE FROM INVENTORY_MOVEMENT WHERE MOVEMENT_ID = ?"
        self.cursor.execute(query, (movement_id,))
        self.conn.commit()
        print(f"Deleted movement record {movement_id}.")

    def delete_client(self, client_id):
        query = "DELETE FROM CLIENT WHERE CLIENT_ID = ?"
        self.cursor.execute(query, (client_id,))
        self.conn.commit()
        print(f"Deleted client {client_id}.")


    # 4. SIMPLE SELECT

    def get_all_facilities(self):
        query = "SELECT * FROM FACILITY"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print("\n--- All Facilities ---")
        for row in rows:
            print(f"ID: {row.FACILITY_ID}, Zone: {row.ZONE}, Climate Control: {row.CLIMATE_CONTROL}")

    # 5. COMPLEX SELECT WITH 2 left JOIN

    def get_client_storage_totals(self):
        query = """
            SELECT 
                C.CLIENT_ID, 
                C.CLIENT_NAME,  
                SUM(I.QUANTITY_STORED) AS TOTAL_STORED_ITEMS
            FROM 
                CLIENT C
            LEFT JOIN 
                STORAGE_AGREEMENT SA ON C.CLIENT_ID = SA.CLIENT_ID
                LEFT JOIN dbo.INCLUDES I on SA.AGREEMENT_ID = I.AGREEMENT_ID
            GROUP BY 
                C.CLIENT_ID, C.CLIENT_NAME
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        print("\n--- Client Storage Totals (Inquiry 6) ---")
        for row in rows:
            # Handling NULLs in case a client has no agreements yet
            total = row.TOTAL_STORED_ITEMS if row.TOTAL_STORED_ITEMS is not None else 0
            print(f"Client: {row.CLIENT_NAME} | Contact: {row.CONTACT_INFO} | Total Items: {total}")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db = WarehouseDatabase()

    try:

        db.insert_facility(facility_id=102, zone='upper Egypt', climate_control='Yes')
        db.update_facility_climate(facility_id=102, new_climate_status='No')

        db.get_all_facilities()
        db.get_client_storage_totals()



    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close_connection()