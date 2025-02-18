from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import mysql.connector



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///momo_data.db'

@app.route('/')
def home():
    return '<h1>Flask REST api</h1>'

@app.route('/airtime', methods=['GET'])
def get_transactions():
    conn = mysql.connector.connect(
        host='localhost',
        user='group',
        password='group123',
        database='momo_data',
        port = 3306
 
        )

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Airtime')
    transactions = cursor.fetchall()
    conn.close()
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True)