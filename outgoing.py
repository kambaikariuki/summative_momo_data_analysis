import json
import re

# Open the text file and read all lines
with open("outgoing.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

#regex pattern to capture the required details
pattern = re.compile(
    r"\*165\*S\*(\d+) RWF transferred to (.+?) \((\d+)\) from (\d+) at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) . Fee was: (\d+) RWF. New balance: (\d+) RWF"
)

transactions = []

# Loop through each line and get transaction details
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

# Save the extracted data to a JSON file
with open("outgoing.json", "w", encoding="utf-8") as json_file:
    json.dump(transactions, json_file, indent=4)

print("Transactions successfully extracted and saved to outgoing.json!")
