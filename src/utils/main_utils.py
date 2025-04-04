import os
import json
import yaml

def read_yaml_file(filepath: str) -> dict:
    """Read a YAML file and return a dictionary."""
    try:
        with open(filepath, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise Exception(f"Error reading YAML file {filepath}: {str(e)}")

def save_json(filepath: str, data: dict):
    """Save dictionary data as a JSON file."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise Exception(f"Error saving JSON file {filepath}: {str(e)}")
