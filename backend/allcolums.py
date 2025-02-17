import sqlite3

conn = sqlite3.connect("transactions.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(transactions);")
columns = cursor.fetchall()

for column in columns:
    print(column)

conn.close()

