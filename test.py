import os
import yaml
import json
from shutil import copyfile

def read_manifest_folders(root_folder):
    # Create folders for storing YAML and JSON files
    if not os.path.exists("manifest_yaml"):
        os.makedirs("manifest_yaml")
    if not os.path.exists("manifest_json"):
        os.makedirs("manifest_json")
    
    # Iterate through each folder in the root directory
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            # Open template folder in each folder
            template_folder = os.path.join(folder_path, "template")
            if os.path.exists(template_folder):
                # Copy app_definition_mf.yml file to manifest_yaml folder with foldername_filename.yaml
                source_file = os.path.join(template_folder, "app_definition_mf.yml")
                dest_file = os.path.join("manifest_yaml", f"{folder_name}_app_definition_mf.yaml")
                copyfile(source_file, dest_file)
                
                # Convert YAML to JSON and save in manifest_json folder
                with open(source_file, 'r') as yaml_file:
                    yaml_data = yaml.safe_load(yaml_file)
                    json_data = json.dumps(yaml_data, indent=4)
                    json_filename = f"{folder_name}_app_definition_mf.json"
                    json_filepath = os.path.join("manifest_json", json_filename)
                    with open(json_filepath, 'w') as json_file:
                        json_file.write(json_data)

# Specify the root folder containing manifest folders
root_folder = "path/to/root/folder"

# Call the function to read manifest folders and perform the tasks
read_manifest_folders(root_folder)
