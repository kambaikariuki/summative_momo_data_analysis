from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('momo_data.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

# API endpoint: Fetch all transactions
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return jsonify([dict(transaction) for transaction in transactions])

# API endpoint: Fetch a single transaction by ID
@app.route('/api/transactions/<int:id>', methods=['GET'])
def get_transaction(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE id = ?', (id,))
    transaction = cursor.fetchone()
    conn.close()
    if transaction is None:
        return jsonify({'error': 'Transaction not found'}), 404
    return jsonify(dict(transaction))

# API endpoint: Add a new transaction
@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (type, amount, date, sender, recipient)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['type'], data['amount'], data['date'], data['sender'], data['recipient']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Transaction added successfully'}), 201

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
