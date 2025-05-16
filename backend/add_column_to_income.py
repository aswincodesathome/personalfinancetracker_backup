import sqlite3

# Step 1: Connect to your SQLite DB
conn = sqlite3.connect('finance_tracker.db')
cursor = conn.cursor()

# Step 2: Alter table to add the missing column
try:
    cursor.execute("ALTER TABLE income ADD COLUMN received_on DATE;")
    print("✅ Column 'received_on' added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️ Error:", e)

# Step 3: Save and close
conn.commit()
conn.close()
