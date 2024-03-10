import pymysql

# Connect to MySQL server
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Execute SQL query to drop the database
        cursor.execute('DROP DATABASE IF EXISTS japanet')
    
    # Commit the transaction
    connection.commit()

finally:
    # Close the connection
    connection.close()
