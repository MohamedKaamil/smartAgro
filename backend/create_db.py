import mysql.connector
from mysql.connector import Error

try:
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        port=3306
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS crop_recommendation")
        print("Database 'crop_recommendation' created successfully!")
        
        cursor.close()
        
except Error as e:
    print(f"Error: {e}")
    
finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")