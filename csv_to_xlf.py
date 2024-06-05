import csv
import xml.etree.ElementTree as ET
import os
import argparse

def create_xlf_file(input_file, output_file, target_lang):
    """
    Convert a CSV file to an XLF file.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to the output XLF file.
        target_lang (str): Target language code.
    """
    # Open the CSV file
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)

    # Create the root element
    root = ET.Element('xliff')
    root.set('version', '1.2')

    # Create the file element
    file_elem = ET.SubElement(root, 'file')
    file_elem.set('original', 'source')
    file_elem.set('datatype', 'plaintext')
    file_elem.set('source-language', 'en')
    file_elem.set('target-language', target_lang)

    # Create the body element
    body_elem = ET.SubElement(file_elem, 'body')

    # Iterate through the data rows
    for i, row in enumerate(data[1:], start=1):  # Skip the header row and start from 1
        # Create the trans-unit element
        trans_unit = ET.SubElement(body_elem, 'trans-unit')
        trans_unit.set('id', str(i))
        trans_unit.set('resname', f'resource{i}')

        # Add the source element
        source_elem = ET.SubElement(trans_unit, 'source')
        source_elem.text = row[0]

        # Add the target element
        target_elem = ET.SubElement(trans_unit, 'target')
        target_elem.text = row[1]

    # Write the XML tree to the output file with proper indentation
    xml_string = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    formatted_xml = xml_string.decode('utf-8').replace('><', '>\n<')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(formatted_xml)

    print("XLF file created successfully!")

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert CSV to XLF')
    parser.add_argument('--input', type=str, required=True, help='Input CSV file path')
    parser.add_argument('--lang', type=str, required=True, help='Target language code')
    args = parser.parse_args()

    input_file = args.input
    target_lang = args.lang

    # Get the input file name without extension
    input_file_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"out/{input_file_name}.xlf"

    create_xlf_file(input_file, output_file, target_lang)