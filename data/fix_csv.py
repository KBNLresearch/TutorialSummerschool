import re
import pandas as pd

input_file = 'DeStandaard_1873.csv'  # Replace with your input CSV file path
output_file = 'DeStandaard_1873_fixed.csv'  # Replace with your output CSV file path

# input_file = 'DeTijd_1873.csv'  # Replace with your input CSV file path
# output_file = 'DeTijd_1873_fixed.csv'  # Replace with your output CSV file path
#
# input_file = 'HetVaderland_1873.csv'  # Replace with your input CSV file path
# output_file = 'HetVaderland_1873_fixed.csv'  # Replace with your output CSV file path

def fix_content_line(line):
    line_until_date, date_field, line_after_date = split_on_date_field(line)
    # if line[:5] == '13792':
    #     print("line ", line[:5])

    row = line_after_date.strip().split(',')  # Split line into parts by comma
    # sed -n '19p' DeTijd_1873_fixed.csv
    # Assuming columns 1-6 and 8-9 are correct, and only column 7 needs fixing

    column7 = row[:-2]  # Supposed content column
    after_column7 = row[-2:]  # Supposed columns 8, 9

    before_content = line_until_date + date_field + ','
    # Combine the parts after column 6 and before column 9 as column 7
    if column7 is None or column7 == []:
        print('geen content')
        content = ''
    else:
        content = ','.join(column7)
    after_content = ',' + ','.join(after_column7)

    escaped_content = content

    # remove any starting and ending quotes to start correcting the inner quotes.
    if escaped_content.startswith('"'):
        escaped_content = escaped_content[1:]  # Remove satrting quote
    if escaped_content.endswith('"'):
        escaped_content = escaped_content[:-1] # Remove ending quote

    # make sure any quotes are being doublequoted when they belong to the content
    escaped_content = escaped_content.replace('"', '""')

    # Put quotes around the content
    if ',' in escaped_content:
        escaped_content = '"' + escaped_content + '"'

    # concat the line parts
    corrected_line = before_content + escaped_content + after_content

    return corrected_line

def split_on_date_field(line):
    # Define the regex pattern to match the date field
    date_pattern = r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}'

    # Find the position of the date field in the line
    match = re.search(date_pattern, line)
    if not match:
        return None, None  # Return None if the date field is not found

    date_pos = match.start()

    # Split the line into two parts based on the position of the date field
    line_until_date = line[:date_pos]
    line_after_date = line[date_pos + len(match.group()):].lstrip(',')

    return line_until_date, match.group(), line_after_date


# Read input CSV, fix escaping of content column, and write to output CSV
with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
        open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    header = infile.readline().strip().split(',')  # Read and process header
    outfile.write(','.join(header) + '\n')  # Write the header to the output file

    for line in infile:
        corrected_line = fix_content_line(line)
        if corrected_line:
            outfile.write(corrected_line + '\n')
            print("Corrected line:", corrected_line + '\n')

data = pd.read_csv(output_file, index_col=0, delimiter=',', encoding='utf-8', quotechar='"', quoting=0)

# Print the DataFrame to verify the content
print(data)
