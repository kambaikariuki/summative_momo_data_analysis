import json
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='group',
    password='group123',
    database='momo_data'
)

cursor = conn.cursor()

# Airtime DONE
with open('backend/json/airtime_bill.json', 'r') as file:
    airtime = json.load(file)

for item in airtime:
    sql = '''
        INSERT INTO Airtime (Transaction_ID, Amount, Date) 
        VALUES (%s, %s, %s);
        '''
    values = (item['transaction_id'], item['amount'], item['date_time'])
    cursor.execute(sql, values)

# Bank deposits DONE
with open('backend/json/bank_deposit.json', 'r') as file:
    deposits = json.load(file)

for item in deposits:
    sql = '''
        INSERT INTO Bank_Deposits (Amount, Date) 
        VALUES (%s, %s);
        '''
    values = (item['amount'], item['date_time'])
    cursor.execute(sql, values)

# Bundle purchase DONE
with open('backend/json/bundle_purchase.json', 'r') as file:
    bundles = json.load(file)

for item in bundles:
    sql = '''
        INSERT INTO Bundle_Purchases (Amount, Date) 
        VALUES (%s, %s);
        '''
    values = (item['amount'], item['date_time'])
    cursor.execute(sql, values)

# Cash power DONE
with open('backend/json/cash_power.json', 'r') as file:
    cash_power = json.load(file)

for item in cash_power:
    sql = '''
        INSERT INTO Cash_Power (Amount, Date) 
        VALUES (%s, %s);
        '''
    values = (item['amount'], item['date_time'])
    cursor.execute(sql, values)

# Code payments DONE
with open('backend/json/code_payments.json', 'r') as file:
    code_pay = json.load(file)

for item in code_pay:
    sql = '''
        INSERT INTO Code_Payments (Transaction_ID, Code_number, Code_name, Amount, Date) 
        VALUES (%s, %s, %s, %s, %s);
        '''
    values = (item['transaction_id'], item['code_number'], item['code_holder'], item['amount'], item['date_time'])
    cursor.execute(sql, values)

# Incoming DONE
with open('backend/json/incoming.json', 'r') as file:
    incoming = json.load(file)

for item in incoming:
    sql = '''
        INSERT INTO Incoming (Transaction_ID, Sender_Name, Amount, Date) 
        VALUES (%s, %s, %s, %s);
        '''
    values = (item['transaction_id'], item['sender_details'], item['amount_received'], item['date_time'])
    cursor.execute(sql, values)

# Outgoing DONE
with open('backend/json/outgoing.json', 'r') as file:
    outgoing = json.load(file)

for item in outgoing:
    sql = '''
        INSERT INTO Outgoing (Recipient_Name, Amount, Date) 
        VALUES (%s, %s, %s);
        '''
    values = (item['receiver'], item['amount'], item['date'])
    cursor.execute(sql, values)

# Third party DONE
with open('backend/json/third_party.json', 'r') as file:
    third_party = json.load(file)

for item in third_party:
    sql = '''
        INSERT INTO Third_party (Transaction_ID, Third_party_name, Amount, Date) 
        VALUES (%s, %s, %s, %s);
        '''
    values = (item["Financial_Transaction_Id"], item['Receiver'], item['Amount'], item['Date'])
    cursor.execute(sql, values)

# Withdrawals DONE
with open('backend/json/withdrawals.json', 'r') as file:
    withdrawals = json.load(file)

for item in withdrawals:
    sql = '''
        INSERT INTO Withdrawals (Amount, Date, Agent, Agent_Number) 
        VALUES (%s, %s, %s, %s);
        '''
    values = (item['amount'], item['date_time'], item['agent_name'], item['agent_number'])
    cursor.execute(sql, values)

conn.commit()
conn.close()

print("Done. Records saved in db")