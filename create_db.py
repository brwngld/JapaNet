import mysql.connector

# Establish connection to MySQL server
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234'
)

# Create a cursor object to execute SQL queries
my_cursor = mydb.cursor()

# Drop the database if it exists
my_cursor.execute("DROP DATABASE IF EXISTS japanet")

# Create the database
my_cursor.execute("CREATE DATABASE japanet")

# Retrieve the list of databases to verify if 'japanet' was created
my_cursor.execute("SHOW DATABASES")
databases = [db[0] for db in my_cursor.fetchall()]

if 'japanet' in databases:
    print("Database 'japanet' successfully created.")
else:
    print("Failed to create database 'japanet'.")
