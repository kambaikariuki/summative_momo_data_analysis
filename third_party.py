import re
import json

# Read the contents of the file
with open('third_party.txt', 'r') as file:
    data = file.read()

# Regular expression to extract the fields
pattern = r"A transaction of (\d+) RWF by ([\w\s]+) on your MOMO account was successfully completed at ([\d-]+\s[\d:]+).+Your new balance:(\d+) RWF.+Financial Transaction Id: (\d+).+External Transaction Id: ([\w\-]+)"

# Find all matches
matches = re.findall(pattern, data)

# Prepare data for JSON output
transactions = []
for match in matches:
    transaction = {
        "Amount": match[0],
        "Receiver": match[1],
        "Date": match[2],
        "New_Balance": match[3],
        "Financial_Transaction_Id": match[4],
        "External_Transaction_Id": match[5]
    }
    transactions.append(transaction)

# Convert to JSON
json_output = json.dumps(transactions, indent=4)

# Save to a JSON file
with open('third_party.json', 'w') as json_file:
    json_file.write(json_output)

print("Data has been successfully saved to third_party.json")
