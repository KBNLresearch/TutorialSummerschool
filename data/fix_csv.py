import csv


def escape_content(content):
    # Remove the first and last quotes if they exist
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]
    # Fix the escaping for double quotes and commas
    return content.replace('"', '""').replace(',', '\\,')


def fix_escaped_content(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8',
                                                                      newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writeheader()
        for row in reader:
            # Fix the content column
            row['content'] = escape_content(row['content'])
            writer.writerow(row)


# Define the input and output file paths
input_csv = 'path/to/your/input.csv'
output_csv = 'path/to/your/output.csv'

# Fix the CSV file
fix_escaped_content(input_csv, output_csv)
