import xml.etree.ElementTree as ET
import csv
import argparse
import os

def create_csv_from_xlf(input_file, output_file):
    """
    Convert an XLF file to a CSV file.

    Args:
        input_file (str): Path to the input XLF file.
        output_file (str): Path to the output CSV file.
    """
    # Open the .xlf file
    with open(input_file, 'r', encoding='utf-8') as file:
        tree = ET.parse(file)
    root = tree.getroot()

    # Create a list of lists to store the data
    data = []

    # Set to collect all unique attribute names
    attribute_names = set()

    # Iterate through the trans-unit elements to collect attribute names
    for trans_unit in root.findall('.//trans-unit'):
        # Collect attribute names
        for attr in trans_unit.attrib:
            attribute_names.add(attr)

    # Convert the set of attribute names to a sorted list
    attribute_names = sorted(attribute_names)

    # Iterate through the trans-unit elements to collect data
    for trans_unit in root.findall('.//trans-unit'):
        source = trans_unit.find('source').text
        try:
            target = trans_unit.find('target').text
        except AttributeError:
            target = ''
        
        # Collect attribute values in the same order as attribute_names
        attributes = [trans_unit.get(attr, '') for attr in attribute_names]

        # Append source, target, and attributes to the data list
        data.append([source, target] + attributes)

    # Open the CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        header = ['Source', 'Target'] + attribute_names
        writer.writerow(header)

        # Write the data rows
        writer.writerows(data)

    print("CSV file created successfully!")

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert XLF to CSV')
    parser.add_argument('--input', type=str, required=True, help='Input XLF file path')
    args = parser.parse_args()

    input_file = args.input

    # Generate the output file name based on the input file name
    input_file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"out/{input_file_name}.csv"

    create_csv_from_xlf(input_file, output_file)
