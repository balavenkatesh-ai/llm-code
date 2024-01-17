import csv
from io import StringIO

def convert_to_csv(response,csv_filename):

    # Find the start and end indices of the table
    start_index = response.find('| ---')
    end_index = response.find('|', start_index + 1)

    # Extract and clean the table part of the response
    table_data = response[start_index:end_index].strip()

    # Create a CSV file in-memory
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file, delimiter=',')

    # Extract rows from the table data
    rows = table_data.split('\n|')
    rows = [row.strip().strip('|').split('|') for row in rows if row.strip()]

    # Write header and data to CSV
    csv_writer.writerow([item.strip() for item in rows[0]])  # Header
    for row in rows[1:]:
        csv_writer.writerow([item.strip() for item in row])

    # Save CSV to a local file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_file.write(csv_file.getvalue())

    print(f"CSV file saved as {csv_filename}")