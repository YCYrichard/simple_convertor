import xml.etree.ElementTree as ET
import csv

# Open the .xlf file

with open('input/for_translation_xliff_archfx-cloud_archfx-cloud_zh.xlf', 'r', encoding='utf-8') as file:
    tree = ET.parse(file)
root = tree.getroot()
# Create a list of lists to store the data
data = []

# Iterate through the source and target elements
for trans_unit in root.findall('.//trans-unit'):
    source = trans_unit.find('source').text
    try:
        target = trans_unit.find('target').text
    except AttributeError:
        target = ''
    # Get all the attributes of the trans-unit element
    attributes = {}
    for attr in trans_unit.attrib:
        attributes[attr] = trans_unit.attrib[attr]
    
    # Append source, target, and attributes to the data list
    data.append([source, target] + list(attributes.values()))

# Open the CSV file for writing
with open('out/output.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Source', 'Target'])

    # Write the data rows
    writer.writerows(data)

print("CSV file created successfully!")