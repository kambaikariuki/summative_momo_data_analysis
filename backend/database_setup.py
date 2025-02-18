import sqlite3
import json

def create_database(db_path):
    """
    Creates the SQLite database and transactions table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        amount INTEGER NOT NULL,
        sender TEXT,
        recipient TEXT,
        transaction_id TEXT,
        agent_name TEXT,
        agent_phone TEXT,
        bundle_size INTEGER,
        validity_days INTEGER,
        date DATETIME NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def insert_data(db_path, data):
    """
    Inserts the normalized data into the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for record in data:
        category = record.get("category", "")
        amount = record.get("amount", 0)
        sender = record.get("sender", "")
        recipient = record.get("recipient", "")
        transaction_id = record.get("transaction_id", "")
        agent_name = record.get("agent_name", "")
        agent_phone = record.get("agent_phone", "")
        bundle_size = record.get("bundle_size", 0)
        validity_days = record.get("validity_days", 0)
        date = record.get("date", "")

        cursor.execute("""
        INSERT INTO transactions (
            category, amount, sender, recipient, transaction_id, 
            agent_name, agent_phone, bundle_size, validity_days, date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            category, amount, sender, recipient, transaction_id,
            agent_name, agent_phone, bundle_size, validity_days, date
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = "momo.db"  # SQLite database file

    # Step 1: Create the database and table
    create_database(db_path)

    # Step 2: Load normalized data from JSON
    with open("normalized_data.json", "r", encoding="utf-8") as f:
        normalized_data = json.load(f)

    # Convert datetime objects to strings for storage
    for record in normalized_data:
        if isinstance(record.get("date"), str):
            record["date"] = record["date"]
        else:
            record["date"] = record["date"].strftime("%Y-%m-%d %H:%M:%S")

    # Step 3: Insert data into the database
    insert_data(db_path, normalized_data)

    print("Data inserted into the database successfully!")