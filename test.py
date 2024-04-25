import yaml
import pandas as pd
import glob


def flatten_yaml(data, prefix=""):
  """
  Flattens a nested YAML structure into a dictionary.
  """
  result = {}
  for key, value in data.items():
    new_key = prefix + key if prefix else key
    if isinstance(value, dict):
      result.update(flatten_yaml(value, new_key + "_"))
    elif isinstance(value, list):
      result[new_key] = ",".join(map(str, value))  # Join array elements as comma-separated string
    else:
      result[new_key] = value
  return result


# Specify the path to the folder containing YAML files
yaml_folder = "manifest"

# Read all YAML files in the folder
data = []
for yaml_file in glob.glob(yaml_folder + "/*.yml"):
    with open(yaml_file, "r") as file:
        data.append(flatten_yaml(yaml.safe_load(file)))

# Combine data from all YAML files into a DataFrame
df = pd.DataFrame(data)

# Create a single CSV file
df.to_csv("manifest_data.csv", index=False)

print("YAML files successfully converted to CSV!")


Subject: Request for Approval: Transfer of Manifest Files and Master Control File to DevFactory

Dear [Recipient's Name],

I hope this email finds you well.

I am writing to seek your approval for a critical task related to our project. We need to transfer all 240 manifest files along with the master control file to DevFactory. This transfer is essential for storing these files in the vector database and subsequently performing the RAG technique with the Language Model (LLM).

To ensure a smooth transition, I kindly request your guidance on the steps to transfer these files to DevFactory. 
