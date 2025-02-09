import xml.etree.ElementTree as ET 
from lxml import etree

# Using xml.etree.ElementTree for debugging:
tree_et = ET.parse('modified_sms_v2.xml')
root_et = tree_et.getroot()

# Print XML structure (from ElementTree)
print(ET.tostring(root_et, encoding='utf8').decode('utf8'))

# Note: element.text is None because SMS content is in the "body" attribute:
for element in root_et.findall('sms'):
    print(element.text)  # Will print None

# Now using lxml:
tree = etree.parse('modified_sms_v2.xml')
root = tree.getroot()

# Use XPath to reliably find all <sms> elements
sms_elements = root.xpath(".//sms")
for element in sms_elements:
    # element.text will be None; content is in the "body" attribute
    print(element.get("body"))

# Extract SMS Messages using the body attribute
messages = [msg.get("body").strip() for msg in sms_elements if msg.get("body")]
print("Extracted Messages:", messages)

# For debugging, catch missing "body" attributes
for element in root_et.findall('sms'):
    body = element.get("body")
    if body:
        print(body.strip())
    else:
        print("Missing 'body' attribute in sms element.")


# Categorize messages (remains the same)
categories = {
    "Incoming Money": ["received", "credited", "deposit"],
    "Payments to Code Holders": ["paid to", "merchant payment"],
    "Transfers to Mobile Numbers": ["sent to", "transfer"],
    "Bank Deposits": ["bank deposit", "account credited"],
    "Airtime Bill Payments": ["airtime purchase", "recharged"],
    "Cash Power Bill Payments": ["electricity payment", "cash power"],
    "Transactions Initiated by Third Parties": ["sent on behalf", "third party"],
    "Withdrawals from Agents": ["withdrawn", "cashout"],
    "Bank Transfers": ["bank transfer", "moved to account"],
    "Internet and Voice Bundle Purchases": ["internet bundle", "voice bundle"]
}
categorized_messages = {category: [] for category in categories}

for msg in messages:
    for category, keywords in categories.items():
        if any(keyword in msg.lower() for keyword in keywords):
            categorized_messages[category].append(msg)
            break  # Stop checking once a category is found

# Print categorized messages
for category, msgs in categorized_messages.items():
    print(f"\n{category}:")
    for m in msgs:
        print(f"- {m}")
