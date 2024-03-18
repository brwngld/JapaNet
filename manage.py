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

# Execute SQL query to retrieve all tables
cursor.execute("SHOW TABLES")

# Fetch all rows from the result set
tables = cursor.fetchall()

# Print the list of tables (models)
print("List of tables (models):")
for table in tables:
    print(table[0])

# Close cursor and connection
cursor.close()
conn.close()