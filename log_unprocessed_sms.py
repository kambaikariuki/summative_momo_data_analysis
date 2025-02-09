import xml.etree.ElementTree as ET
import re
import logging

# Configure logging
logging.basicConfig(filename="error_log.txt", level=logging.WARNING, format="%(asctime)s - %(message)s")

# Function to categorize SMS messages
def categorize_sms(message):
    categories = {
        "Incoming Money": r"received (\d+ RWF) from",
        "Payments to Code Holders": r"payment of (\d+ RWF) to [A-Za-z ]+ has been completed",
        "Airtime Purchase": r"purchased an internet bundle|Airtime",
        "Withdrawals": r"withdrawn (\d+ RWF) on",
        "Bank Transfers": r"bank transfer of (\d+ RWF) to",
        "Others": r".*"  # Catch-all for other messages
    }

    for category, pattern in categories.items():
        if re.search(pattern, message, re.IGNORECASE):
            return category
    
    return None  # Message doesn't match known categories

# Function to process XML data
def process_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        processed_data = []

        for sms in root.findall("sms"):
            body = sms.find("body").text.strip() if sms.find("body") is not None else ""

            category = categorize_sms(body)
            if category:
                processed_data.append({"message": body, "category": category})
            else:
                # Log unprocessed messages
                logging.warning(f"Unprocessed SMS: {body}")

        return processed_data

    except Exception as e:
        logging.error(f"Error processing XML file: {str(e)}")

# Example usage
xml_file = "modified_sms_v2.xml"  # Update with your file path
processed_messages = process_xml(xml_file)

# Print results
for msg in processed_messages:
    print(f"Category: {msg['category']} - Message: {msg['message']}")

print("Processing complete. Check error_log.txt for unprocessed messages.")

