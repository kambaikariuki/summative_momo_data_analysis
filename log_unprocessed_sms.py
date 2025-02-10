import logging

# Set up logging
logging.basicConfig(
    filename='unprocessed_messages.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Sample data (replace with your actual message data)
sms_data = [
    {"address": "M-Money", "date": 1717691653000, "body": "Some body content", "status": -1, "read": 0},
    {"address": "M-Money", "date": 1717739543710, "body": "*113*R*A bank deposit of 5000 RWF...", "status": -1, "read": 1},
    {"address": "M-Money", "date": 1717937937200, "body": "*162*TxId:14303889432*S*Your payment of 2000 RWF...", "status": -1, "read": 1},
    # Add other messages...
]

# Function to process and log unprocessed messages
def process_sms_messages(messages):
    for message in messages:
        # Example of processing logic
        if message['status'] == -1 and message['read'] == 0:
            # Log unprocessed/ignored messages
            logging.info(f"Unprocessed message: {message}")
            print(f"Unprocessed message logged: {message}")

# Call the function to process the messages
process_sms_messages(sms_data)
