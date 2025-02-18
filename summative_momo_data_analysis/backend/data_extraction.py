import xml.etree.ElementTree as ET

def extract_sms_data(xml_file):
    # Load the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Debug: Print the root tag to confirm the structure
    print(f"Root tag: {root.tag}")

    # Extract all <sms> elements
    sms_data = []
    for sms in root.findall('sms'):  # Adjust 'sms' if necessary
        body = sms.get('body')  # Get the 'body' attribute
        if body:
            sms_data.append(body.strip())
        else:
            print("Warning: Missing or empty 'body' attribute in an <sms> element.")

    return sms_data

if __name__ == "__main__":
    xml_file = "modified_sms_v2.xml"  # Replace with your XML file path
    sms_data = extract_sms_data(xml_file)

    print(f"Total SMS messages extracted: {len(sms_data)}")
    # Save extracted data to a file for debugging
    with open("extracted_sms.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sms_data))

    # Debug: Print the first few SMS messages
    if sms_data:
        print("First 5 extracted SMS messages:")
        for i, sms in enumerate(sms_data[:5], start=1):
            print(f"{i}. {sms}")
    else:
        print("No SMS messages were extracted.")