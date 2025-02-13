import json
import re


pattern = re.compile(
    r"You have received (\d+) RWF from (.+?) \(\*+\d+\) on your mobile money account at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?Your new balance:(\d+) RWF.*?Financial Transaction Id: (\d+).")


with open("Incoming.txt", "r") as file:
    incoming_data_text = file.read()


transactions = []

# Extracting data using the regular expression pattern
for match in pattern.finditer(incoming_data_text):
    amount, sender_details, date_time, new_balance, transaction_id = match.groups()
    transactions.append({
        "amount_received": int(amount),
        "sender_details": sender_details.strip(),
        "date_time": date_time,
        "new_balance": int(new_balance),
        "transaction_id": transaction_id})

# Saving the extracted data to a JSON file: transactions.json
with open("incoming.json", "w") as json_file:
    json.dump(transactions, json_file, indent=4)

print("Data has been successfully saved to incoming.json!")