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


I've conducted two experiments with different formats of manifest files: JSON and CSV. I created two collections in the vector database and tested both experiments with the same questions.

In the experiment using JSON format, the Language Model (LLM) couldn't extract the correct item ID from the JSON. However, when I used CSV format, the LLM successfully extracted the correct item ID from the context.

To troubleshoot this experiment, I utilized LangSmith. I've attached the results of both experiments below for your review.
