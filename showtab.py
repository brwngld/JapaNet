import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="japanet"
)

# Create a cursor object
cursor = conn.cursor()

# Execute DESCRIBE statement
table_name = "Addproduct"
cursor.execute(f"DESCRIBE {table_name}")

# Fetch and print the results
columns = cursor.fetchall()
for column in columns:
    print(column)

# Close cursor and connection
cursor.close()
conn.close()
