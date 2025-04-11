import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root@123',  # 🔑 CHANGE THIS to your real MySQL root password
        database='finance_tracker'

    )
    return connection
