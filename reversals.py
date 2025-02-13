import json
import re

# Open the text file and read all lines
with open("reversals.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Define regex pattern to capture the reversal details
pattern = re.compile(
    r"Your transaction to (.+?) \((\d+)\) with (\d+) RWF has been reversed at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}). Your new balance is (\d+) RWF"
)

reversals = []

# Loop through each line and extract reversal details
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

# Save the extracted data to a JSON file
with open("reversals.json", "w", encoding="utf-8") as json_file:
    json.dump(reversals, json_file, indent=4)

print("Reversal transactions successfully extracted and saved to reversals.json!")
