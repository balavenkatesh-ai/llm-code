import os
import yaml
import csv

def read_yaml_files(folder_path):
    all_yaml_data = []

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as yaml_file:
                try:
                    yaml_data = yaml.safe_load(yaml_file)
                    all_yaml_data.append(yaml_data)
                except yaml.YAMLError as e:
                    print(f"Error reading file '{filename}': {e}")

    return all_yaml_data

def write_to_csv(yaml_data_list, csv_file_path):
    if not yaml_data_list:
        print("No YAML data found.")
        return
    
    # Extract fieldnames from all YAML files
    fieldnames = set()
    for yaml_data in yaml_data_list:
        fieldnames.update(yaml_data.keys())

    # Write YAML data to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=sorted(fieldnames))
        writer.writeheader()
        for yaml_data in yaml_data_list:
            writer.writerow(yaml_data)

def convert_yaml_to_csv(folder_path, csv_file_path):
    yaml_data_list = read_yaml_files(folder_path)
    write_to_csv(yaml_data_list, csv_file_path)

# Specify the folder containing YAML files and the CSV file path
folder_path = "path/to/yaml/folder"
csv_file_path = "output.csv"

# Call the function to convert YAML to CSV
convert_yaml_to_csv(folder_path, csv_file_path)
