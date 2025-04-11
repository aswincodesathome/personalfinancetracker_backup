# backend/test_db.py

from config import DB_CONFIG
import mysql.connector

try:
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )
    print("✅ Connected to MySQL database successfully!")
    conn.close()
except mysql.connector.Error as err:
    print("❌ Database connection failed:", err)
