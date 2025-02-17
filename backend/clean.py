import xml.etree.ElementTree as ET
import re
import json
import sqlite3
import sqlite3


conn = sqlite3.connect('transactions.db')

cursor = conn.cursor()

# Parse XML file into Element tree

def get_body():
    '''Gets the body attribute of each sms and saves them into a list, then to a file'''
    tree = ET.parse('backend/modified_sms_v2.xml')
    root = tree.getroot()

    selected_attributes = [child.get("body") for child in root]

    with open('backend/sms.txt', 'w') as f:
        for item in selected_attributes:
            f.write(str(item) + "\n")


def organize():
    """
    Sorts all the messages into different categories, saves them to txt files
    """

    categories = {
    'incoming' : [],
    'outgoing' : [],
    'code_payments' : [],
    'bank_deposit' : [],
    'withdrawals' : [],
    'cash_power' : [],
    'other' : [],
    'airtime_bill' : [],
    'bundle_purchase': [],
    'third_party' : [],
    'failed' : [],
    'reversals' : []
    }
    code_pattern = r"([A-Z][a-z]+ [A-Z][a-z]+ \d{5})"
    logged = 0
    unlogged = 0

    with open('backend/sms.txt', 'r') as f:
        for line in f:
            if "failed" in line:
                categories['failed'].append(line)
                logged += 1
            else:
                if "received" in line:
                    categories['incoming'].append(line)
                    logged += 1
                elif re.search(code_pattern, line):
                    categories['code_payments'].append(line)
                    logged += 1
                elif "transferred" in line:
                    categories['outgoing'].append(line)
                    logged += 1
                elif "bank deposit" in line:
                    categories['bank_deposit'].append(line)
                    logged += 1
                elif "Airtime" in line:
                    categories['airtime_bill'].append(line)
                    logged += 1
                elif "Bundles and Packs" in line:
                    categories['bundle_purchase'].append(line)
                    logged += 1
                elif "Y'ello" in line:
                    if "Data" in line:
                        categories['bundle_purchase'].append(line)
                    else:
                        categories['third_party'].append(line)
                    logged += 1
                elif "withdrawn" in line:
                    categories['withdrawals'].append(line)
                    logged += 1
                elif "Cash Power" in line:
                    categories['cash_power'].append(line)
                    logged += 1
                elif "Yello!" in line:
                    categories['other'].append(line)
                    logged += 1
                elif "revers" in line:
                    categories['reversals'].append(line)
                    logged += 1
                else:
                    categories['other'].append(line)
                    unlogged += 1
 
    for category, messages in categories.items():
        file = f'backend/txt/{category}.txt'
        with open(file, "w") as f:
            for message in messages:
                f.write(message)

    print(f"Successfully logged {logged} messages, {unlogged} others saved in other.txt")

def to_json():
    """
    Extracts transaction details from .txt files using a regex pattern
    and writes the data to .json files. 
    """

# Airtime

    pattern = re.compile(
    r"\*162\*TxId:(\d+)\*S\*Your payment of ([\d,]+) RWF to Airtime with token .*? has been completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.")

    transactions = []
    transactions_to_update = []

    with open("backend/txt/airtime_bill.txt", "r") as file:
        data = file.read()

    for match in pattern.finditer(data):
        transaction_id, amount, date_time = match.groups()
        amount = amount.replace(",", "")
        transactions.append({
            "transaction_id": transaction_id,
            "amount": int(amount),
            "date_time": date_time
        })
    

    with open("backend/json/airtime_bill.json", "w") as json_file:
        json.dump(transactions, json_file, indent=4)
        transactions_to_insert = [
            (transaction['transaction_id'], 'airtime', transaction['amount'], transaction["date_time"])
            for transaction in transactions
        ]
        cursor.executemany('''
            INSERT INTO transactions (transaction_id ,type, amount, date)
            VALUES (?, ?, ?, ?)
            ''', transactions_to_insert)



# Bank Deposit
    pattern = re.compile(
        r"A bank deposit of (\d+) RWF has been added to your mobile money account at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?Your NEW BALANCE :(\d+) RWF")

    with open("backend/txt/bank_deposit.txt", "r") as file:
        data = file.read()

    transactions = []

    for match in pattern.finditer(data):
        amount, date_time, new_balance = match.groups()
        transactions.append({
            "amount": int(amount),
            "date_time": date_time,
            "new_balance": int(new_balance)
            }
            )

    with open("backend/json/bank_deposit.json", "w") as json_file:
        json.dump(transactions, json_file, indent=4)
        transactions_to_insert = [
            ('bank_deposit', transaction['amount'], transaction["date_time"])
            for transaction in transactions
        ]
        cursor.executemany('''
            INSERT INTO transactions (type, amount, date)
            VALUES (?, ?, ?)
            ''', transactions_to_insert)

# Bundle purchase
    pattern = re.compile(
        r"(?:Your payment of|A transaction of) (\d+) RWF .*? completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    )

    with open("backend/txt/bundle_purchase.txt", "r") as file:
        data = file.read()

    transactions = []

    for match in pattern.finditer(data):
        amount, date_time = match.groups()
        transactions.append({
            "amount": int(amount),
            "date_time": date_time
            }
            )

    with open("backend/json/bundle_purchase.json", "w") as json_file:
        json.dump(transactions, json_file, indent=4)
        transactions_to_insert = [
            ('bundles', transaction['amount'], transaction["date_time"])
            for transaction in transactions
        ]
        cursor.executemany('''
            INSERT INTO transactions (type, amount, date)
            VALUES (?, ?, ?)
            ''', transactions_to_insert)


# Cash Power
    pattern = re.compile(
        r"Your payment of (\d+) RWF .*? completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")

    with open("backend/txt/cash_power.txt", "r") as file:
        data = file.read()

    transactions = []

    for match in pattern.finditer(data):
        amount, date_time = match.groups()
        transactions.append({
            "amount": int(amount),
            "date_time": date_time
            }
            )
        
    with open("backend/json/cash_power.json", "w") as json_file:
        json.dump(transactions, json_file, indent=4)
        transactions_to_insert = [
            ('cash power', transaction['amount'], transaction["date_time"])
            for transaction in transactions
        ]
        cursor.executemany('''
            INSERT INTO transactions (type, amount, date)
            VALUES (?, ?, ?)
            ''', transactions_to_insert)


# Code payments
    pattern = re.compile(r"TxId: (\d+)\. Your payment of ([\d,]+) RWF to ([A-Za-z ]+) (\d+) has been completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.")

    with open("backend/txt/code_payments.txt", "r") as file:
        data = file.read()

    transactions = []

    for match in pattern.finditer(data):
        transaction_id, amount, code_holder, code_number, date_time = match.groups()
        amount = amount.replace(",", "")
        transactions.append({
            "transaction_id": transaction_id,
            "amount": int(amount),
            "code_holder": code_holder,
            "code_number": code_number,
            "date_time": date_time
        })

    with open("backend/json/code_payments.json", "w") as json_file:
        json.dump(transactions, json_file, indent=4)
        transactions_to_insert =[
            (transaction['transaction_id'], 'code_payment', transaction['amount'], transaction['code_holder'], transaction['code_number'], transaction["date_time"])
            for transaction in transactions
        ]
        cursor.executemany('''
            INSERT INTO transactions (transaction_id, type, amount, code_holder, code_number, date)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', transactions_to_insert)

# Incoming
    pattern = re.compile(
        r"You have received (\d+) RWF from (.+?) \(\*+\d+\) on your mobile money account at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?Your new balance:(\d+) RWF.*?Financial Transaction Id: (\d+).")

    with open("backend/txt/incoming.txt", "r") as file:
        incoming_data_text = file.read()

    transactions = []

    for match in pattern.finditer(incoming_data_text):
        amount, sender_details, date_time, new_balance, transaction_id = match.groups()
        transactions.append({
            "amount_received": int(amount),
            "sender": sender_details.strip(),
            "date_time": date_time,
            "new_balance": int(new_balance),
            "transaction_id": transaction_id})

    with open("backend/json/incoming.json", "w") as json_file:
        json.dump(transactions, json_file, indent=4)
        transactions_to_insert = [
            (transaction['transaction_id'], 'incoming', transaction['amount_received'], transaction["date_time"])
            for transaction in transactions
        ]
        cursor.executemany('''
            INSERT INTO transactions (transaction_id, type, amount, date)
            VALUES (?, ?, ?, ?)
            ''', transactions_to_insert)

# Outgoing
    with open("backend/txt/outgoing.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    pattern = re.compile(
        r"\*165\*S\*(\d+) RWF transferred to (.+?) \((\d+)\) from (\d+) at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) . Fee was: (\d+) RWF. New balance: (\d+) RWF"
    )

    transactions = []

    for line in lines:
        match = pattern.search(line)
        if match:
            amount, receiver, phone, sender, date, time, fee, balance = match.groups()
            transactions.append({
                "amount": int(amount),
                "receiver": receiver,
                "phone": phone,
                "sender": sender,
                "date": date,
                "time": time,
                "fee": int(fee),
                "balance": int(balance)
            })

    with open("backend/json/outgoing.json", "w", encoding="utf-8") as json_file:
        json.dump(transactions, json_file, indent=4)

# Reversals 
    with open("backend/txt/reversals.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    pattern = re.compile(
        r"Your transaction to (.+?) \((\d+)\) with (\d+) RWF has been reversed at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}). Your new balance is (\d+) RWF"
    )

    reversals = []

    for line in lines:
        match = pattern.search(line)
        if match:
            receiver, phone, amount, date, time, new_balance = match.groups()
            reversals.append({
                "receiver": receiver,
                "phone": phone,
                "amount": int(amount),
                "date": date,
                "time": time,
                "new_balance": int(new_balance)
            })

    with open("backend/json/reversals.json", "w", encoding="utf-8") as json_file:
        json.dump(reversals, json_file, indent=4)
        reversals_to_insert = [
            ('reversal', reversal['amount'], reversal['receiver'], reversal['date'])
            for reversal in reversals
        ]
        cursor.executemany('''
            INSERT INTO transactions (type, amount, sender, date)
            VALUES (?, ?, ?, ?)
            ''', reversals_to_insert)
                

# Third Party transactions
    with open('backend/txt/third_party.txt', 'r') as file:
        data = file.read()

    pattern = r"A transaction of (\d+) RWF by ([\w\s]+) on your MOMO account was successfully completed at ([\d-]+\s[\d:]+).+Financial Transaction Id: (\d+).+External Transaction Id: ([\w\-]+)"

    matches = re.findall(pattern, data)

    transactions = []
    for match in matches:
        transaction = {
            "Amount": match[0],
            "Receiver": match[1],
            "Date": match[2],
            "transaction_id": match[3]
        }
        transactions.append(transaction)

    json_output = json.dumps(transactions, indent=4)
    transactions_to_insert = [
        ('third_party', transaction['Amount'], transaction['Receiver'], transaction['Date'], transaction['transaction_id'])
        for transaction in transactions
    ]
    cursor.executemany('''
        INSERT INTO transactions (type, amount, sender, date, transaction_id)
        VALUES (?, ?, ?, ?, ?)
        ''', transactions_to_insert)

    with open('backend/json/third_party.json', 'w') as json_file:
        json_file.write(json_output)

# Withdrawals
    pattern = re.compile(
        r"You Abebe Chala CHEBUDIE \(\*+\d+\) have via agent: (?:Agent\s)([\w\s]+) \((\d+)\), withdrawn ([\d,]+) RWF .*? at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) .*? Fee paid: ([\d,]+) RWF.*?Financial Transaction Id: (\d+)\."
    )

    with open("backend/txt/withdrawals.txt", "r") as file:
        data = file.read()

    transactions = []

    for match in pattern.finditer(data):
        agent_name, agent_number, amount, date_time, fee, transaction_id = match.groups()
        amount = amount.replace(",", "")
        fee = fee.replace(",", "")
        transactions.append({
            "agent_name": agent_name,
            "agent_number": agent_number,
            "amount": int(amount),
            "date_time": date_time,
            "fee": int(fee),
            "transaction_id": transaction_id
        })

    with open("backend/json/withdrawals.json", "w") as json_file:
        json.dump(transactions, json_file, indent=4)
        transactions_to_insert = [
            ('incoming', transaction['amount'], transaction['date_time'], transaction['transaction_id'])
            for transaction in transactions
        ]
        cursor.executemany('''
            INSERT INTO transactions (type, amount, date, transaction_id)
            VALUES (?, ?, ?, ?)
            ''', transactions_to_insert)
    conn.commit()

if __name__ == "__main__":
    get_body()
    organize()
    to_json()