import re
from datetime import datetime
import logging
import json

# Configure logging
logging.basicConfig(filename='unmatched_sms.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def categorize_sms(sms_body):
    """
    Categorizes the SMS message based on predefined patterns.
    Returns a dictionary with the category, extracted details, and original SMS body.
    """
    patterns = {
        "Incoming Money": r"You have received (\d+,?\d*) RWF from (.+?)\s?\(.*?\)\s?on your mobile money account at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        "Payments to Code Holders": r"TxId: (\d+)\. Your payment of (\d+,?\d*) RWF to (.+?) \d+ has been completed at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        "Transfers to Mobile Numbers": r"\*165\*S\*(\d+,?\d*) RWF transferred to (.+?) \(.*?\) from \d+ at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        "Bank Deposits": r"\*113\*R\*A bank deposit of (\d+,?\d*) RWF has been added to your mobile money account at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        "Withdrawals from Agents": r"You (.+?) have via agent: (.+?) \((\d+)\), withdrawn (\d+,?\d*) RWF on (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})",
        "Internet and Voice Bundle Purchases": r"You have purchased an internet bundle of (\d+)GB for (\d+,?\d*) RWF valid for (\d+) days"
    }
    
    for category, pattern in patterns.items():
        match = re.search(pattern, sms_body)
        if match:
            return {"category": category, "details": match.groups(), "sms_body": sms_body}
    
    # Log unmatched SMS body
    logging.debug(f"Unmatched SMS: {sms_body}")
    return {"category": "Unknown", "details": (), "sms_body": sms_body}

def normalize_data(data):
    """
    Normalizes the categorized data into a consistent format.
    Returns a list of dictionaries with cleaned and structured data.
    """
    normalized = []
    for entry in data:
        category = entry["category"]
        details = entry["details"]
        sms_body = entry["sms_body"]
        
        try:
            if category == "Incoming Money":
                amount, sender, date = details
                normalized.append({
                    "category": category,
                    "amount": int(amount.replace(',', '')),
                    "sender": sender,
                    "date": datetime.strptime(date, "%Y-%m-%d %H:%M:%S").isoformat(),
                    "message_body": sms_body
                })
            elif category == "Payments to Code Holders":
                tx_id, amount, recipient, date = details
                normalized.append({
                    "category": category,
                    "amount": int(amount.replace(',', '')),
                    "recipient": recipient,
                    "transaction_id": tx_id,
                    "date": datetime.strptime(date, "%Y-%m-%d %H:%M:%S").isoformat(),
                    "message_body": sms_body
                })
            elif category == "Transfers to Mobile Numbers":
                amount, recipient, date = details
                normalized.append({
                    "category": category,
                    "amount": int(amount.replace(',', '')),
                    "recipient": recipient,
                    "date": datetime.strptime(date, "%Y-%m-%d %H:%M:%S").isoformat(),
                    "message_body": sms_body
                })
            elif category == "Bank Deposits":
                amount, date = details
                normalized.append({
                    "category": category,
                    "amount": int(amount.replace(',', '')),
                    "date": datetime.strptime(date, "%Y-%m-%d %H:%M:%S").isoformat(),
                    "message_body": sms_body
                })
            elif category == "Withdrawals from Agents":
                name, agent, agent_phone, amount, date = details
                normalized.append({
                    "category": category,
                    "amount": int(amount.replace(',', '')),
                    "agent_name": agent,
                    "agent_phone": agent_phone,
                    "date": datetime.strptime(date, "%Y-%m-%d %H:%M:%S").isoformat(),
                    "message_body": sms_body
                })
            elif category == "Internet and Voice Bundle Purchases":
                bundle_size, amount, validity_days = details
                normalized.append({
                    "category": category,
                    "bundle_size": int(bundle_size),
                    "amount": int(amount.replace(',', '')),
                    "validity_days": int(validity_days),
                    "message_body": sms_body
                })
        except Exception as e:
            logging.error(f"Error normalizing data: {entry}. Error: {e}")
            continue
    
    return normalized

if __name__ == "__main__":
    # Load extracted SMS data from the previous step
    try:
        with open("extracted_sms.txt", "r", encoding="utf-8") as f:
            sms_data = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        logging.error("extracted_sms.txt not found.")
        raise
    except Exception as e:
        logging.error(f"Error reading extracted_sms.txt: {e}")
        raise
    
    cleaned_data = []
    unprocessed_messages = []
    
    for sms in sms_data:
        result = categorize_sms(sms)
        if result["category"] != "Unknown":
            cleaned_data.append(result)
        else:
            unprocessed_messages.append(sms)
    
    # Normalize the cleaned data
    normalized_data = normalize_data(cleaned_data)
    
    # Save unprocessed messages to a log file
    try:
        with open("unprocessed_messages.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(unprocessed_messages))
    except Exception as e:
        logging.error(f"Error writing unprocessed_messages.txt: {e}")
    
    # Save normalized data to a JSON file for further use
    try:
        with open("normalized_data.json", "w", encoding="utf-8") as f:
            json.dump(normalized_data, f, indent=4)
    except Exception as e:
        logging.error(f"Error writing normalized_data.json: {e}")
    
    print(f"Total SMS messages: {len(sms_data)}")
    print(f"Cleaned messages: {len(cleaned_data)}")
    print(f"Unprocessed messages: {len(unprocessed_messages)}")
    print(f"Normalized messages: {len(normalized_data)}")