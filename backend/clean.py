import xml.etree.ElementTree as ET
import re
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

    categories = {
    'incoming' : [],
    'outgoing' : [],
    'code_payments' : [],
    'bank_deposit' : [],
    'withdrawals' : [],
    'bank_transfer' : [],
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
                    if "Mins" in line:
                        categories['airtime_bill'].append(line)
                    else:
                        categories['bundle_purchase'].append(line)
                    logged += 1
                elif "revers" in line:
                    categories['reversals'].append(line)
                    logged += 1
                else:
                    categories['other'].append(line)
                    unlogged += 1
 
    for category, messages in categories.items():
        file = f'{category}.txt'
        with open(file, "w") as f:
            for message in messages:
                f.write(message)

    print(f"Successfully logged {logged} messages, {unlogged} others saved in other.txt")


