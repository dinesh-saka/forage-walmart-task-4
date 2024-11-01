import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("shipment_database.db")
cursor = conn.cursor()

# Read Spreadsheet 0 and insert into the database
spreadsheet_0 = pd.read_excel("spreadsheet_0.xlsx")
for index, row in spreadsheet_0.iterrows():
    cursor.execute(
        """
        INSERT INTO products (product_name, product_category, quantity)
        VALUES (?, ?, ?)
    """,
        (row["product_name"], row["product_category"], row["quantity"]),
    )

# Read Spreadsheet 1 and 2
spreadsheet_1 = pd.read_excel("spreadsheet_1.xlsx")
spreadsheet_2 = pd.read_excel("spreadsheet_2.xlsx")

# Create a mapping from shipping identifier to origin and destination
shipment_info = {}
for index, row in spreadsheet_2.iterrows():
    shipment_info[row["shipping_id"]] = (row["origin"], row["destination"])

# Process Spreadsheet 1 to combine product data
for index, row in spreadsheet_1.iterrows():
    shipping_id = row["shipping_id"]
    product_name = row["product_name"]
    quantity = row["quantity"]

    # Get origin and destination from shipment_info
    origin, destination = shipment_info.get(shipping_id, (None, None))

    # Insert each product into the database
    cursor.execute(
        """
        INSERT INTO shipments (shipping_id, product_name, quantity, origin, destination)
        VALUES (?, ?, ?, ?, ?)
    """,
        (shipping_id, product_name, quantity, origin, destination),
    )

# Commit changes and close the connection
conn.commit()
conn.close()
