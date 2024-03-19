import os
import yaml
import json

def convert_yaml_to_json(yaml_file, json_file):
    """
    Converts a YAML file to JSON and saves it with the same filename (replacing the '.yaml' extension with '.json').

    Args:
        yaml_file (str): Path to the YAML file.
        json_file (str): Path to the output JSON file.
    """

    try:
        # Open the YAML file in read mode
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)

        # Check if the data is valid YAML (optional)
        if yaml_data is None:
            print(f"Error: '{yaml_file}' is not a valid YAML file.")
            return

        # Convert YAML data to JSON
        json_data = json.dumps(yaml_data, indent=4)  # Add indentation for readability

        # Open the JSON file in write mode (overwrite if it exists)
        with open(json_file, 'w') as f:
            f.write(json_data)

        print(f"Converted '{yaml_file}' to '{json_file}'.")
    except FileNotFoundError:
        print(f"Error: File '{yaml_file}' not found.")
    except PermissionError:
        print(f"Error: Insufficient permissions to access or modify '{yaml_file}'.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def convert_all_yaml_in_directory(directory):
    """
    Converts all YAML files in a directory to JSON and saves them with the same filenames (replacing '.yaml' extension with '.json').

    Args:
        directory (str): Path to the directory containing YAML files.
    """

    for filename in os.listdir(directory):
        if filename.endswith('.yaml'):
            yaml_file = os.path.join(directory, filename)
            json_file = os.path.splitext(yaml_file)[0] + '.json'  # Replace '.yaml' with '.json'
            convert_yaml_to_json(yaml_file, json_file)

if __name__ == '__main__':
    # Example usage
    directory = 'your_directory_path'  # Replace with the path to your directory
    convert_all_yaml_in_directory(directory)