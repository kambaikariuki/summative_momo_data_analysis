import xml.etree.ElementTree as ET

# Parse XML file into Element tree

def get_body():
    '''Gets the body attribute of each sms and saves them into a list, then to a file'''
    tree = ET.parse('backend/modified_sms_v2.xml')
    root = tree.getroot()

    selected_attributes = [child.get("body") for child in root]

    with open('backend/sms.txt', 'w') as f:
        for item in selected_attributes:
            f.write(str(item) + "\n")




get_body()




# new_root = ET.Element('clean_data')

# tags = ["body","readable_date"]

# for tag in tags:
#     for elem in root.findall(f".//{tag}"):
#         new_root.append(elem)

# new_tree = ET.ElementTree(new_root)
# new_tree.write('clean_data.xml')

