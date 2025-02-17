import sqlite3

conn = sqlite3.connect('transactions.db')

cursor = conn.cursor()

# Step 3: Create the 'transactions' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id varchar(100),
    type varchar(100),
    amount REAL NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    sender varchar(100),
    recipient varchar(100)
)
''')

conn.commit()
conn.close()

print("Database and table created successfully!")
