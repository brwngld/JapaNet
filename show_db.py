import mysql.connector

# Connect to MySQL server
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234'
)

# Create a cursor object
my_cursor = mydb.cursor()

# Execute SQL query to retrieve all databases
my_cursor.execute("SHOW DATABASES")

# Fetch all rows from the result set
databases = my_cursor.fetchall()

# Print the list of databases
print("List of databases:")
for db in databases:
    print(db[0])
