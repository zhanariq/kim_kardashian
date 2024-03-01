import xml.etree.ElementTree as ET


def xml_to_dict(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    visited = set()
    insert_values = []

    # Iterate over each <record> element
    for record in root.findall('record'):
        acquirer_id = record.find('MEMBER_ID').text
        if acquirer_id in visited:
            continue
        bin = record.find('BIN').text
        name = record.find('BANK_NAME').text
        country_code = record.find('COUNTRY_CODE').text

        insert_values.append(f"('{acquirer_id}', '{bin}', '{name}', {country_code}),\n")
        visited.add(acquirer_id)

    values = ''.join(insert_values)[:-2] + '\n' # rm last comma
    insert_statement = (
        f"INSERT INTO bank_acquirer_data (acquirer_id, bin, name, country_code) VALUES {values}"
        f"ON CONFLICT (acquirer_id) DO UPDATE SET bin = EXCLUDED.bin, name = EXCLUDED.name, country_code = EXCLUDED.country_code;"
    )
    return insert_statement


if __name__ == '__main__':
    xml_file_path = '1.xml'  # Path to your XML file
    stmt = xml_to_dict(xml_file_path)

    print(stmt)
