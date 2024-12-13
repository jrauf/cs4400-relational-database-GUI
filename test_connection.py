import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="qwerty6920",
    )
    print("Connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
