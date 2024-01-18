import re
import json
import csv
import io

# def convert_to_csv(response,csv_filename):

#     # Extract all JSON data blocks using regular expressions
#     json_data_blocks = re.findall(r'`json(.*?)`', response, flags=re.DOTALL)

#     if json_data_blocks:
#         with open(csv_filename, "w", newline="") as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=None)  # Initialize without headers

#             for json_data_str in json_data_blocks:
#                 try:
#                     json_data = json.loads(json_data_str)

#                     # Write headers only if not already written
#                     if not writer.fieldnames:
#                         writer.fieldnames = list(json_data.keys())
#                         writer.writeheader()

#                     writer.writerow(json_data)

#                 except json.JSONDecodeError:
#                     print(f"Error: Invalid JSON data format in block: {json_data_str}")

#         print("CSV file created successfully!")
#     else:
#         print("Error: No JSON data found in the response.")


def json_to_csv(response):
    """Extracts JSON data from the response and returns a CSV string in memory."""

    csv_data = io.StringIO()
    writer = csv.DictWriter(csv_data, fieldnames=None)

    # Extract JSON blocks using proper JSON parsing
    json_data_blocks = json.loads("[" + response.split("`json")[1].split("`")[0] + "]")

    for json_data in json_data_blocks:
        if not writer.fieldnames:
            writer.fieldnames = list(json_data.keys())
            writer.writeheader()
        writer.writerow(json_data)

    csv_data.seek(0)
    return csv_data.read()
        

def convert_to_csv(response, csv_filename):
    """Extracts JSON data from the response, writes it to a file, and returns a CSV string."""

    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=None)

        # Extract and write JSON blocks to both file and in-memory buffer
        csv_data = io.StringIO()  # Create in-memory buffer
        in_memory_writer = csv.DictWriter(csv_data, fieldnames=None)

        json_data_blocks = re.findall(r'`json(.*?)`', response, flags=re.DOTALL)
        if json_data_blocks:
            for json_data_str in json_data_blocks:
                try:
                    json_data = json.loads(json_data_str)

                    if not writer.fieldnames:
                        writer.fieldnames = list(json_data.keys())
                        in_memory_writer.fieldnames = writer.fieldnames  # Copy headers
                        writer.writeheader()
                        in_memory_writer.writeheader()

                    writer.writerow(json_data)
                    in_memory_writer.writerow(json_data)

                except json.JSONDecodeError:
                    print(f"Error: Invalid JSON data format in block: {json_data_str}")

            csv_data.seek(0)  # Rewind in-memory buffer
            return csv_data.read()  # Return CSV string
        else:
            print("Error: No JSON data found in the response.")
            return None