import mysql.connector
from mysql.connector import Error

def connect_db():
    db_name = "library_management_system"
    username = "root"
    passkey = ""
    host = "127.0.0.1"

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = username,
            password = passkey,
            host = host)
        if conn.is_connected():
            print("Connected to MySql database!")
            return conn
        
    except Error as e:
        print(f"Error = {e}")
        return None