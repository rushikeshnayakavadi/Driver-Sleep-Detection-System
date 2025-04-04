import os
import json
import yaml
from tensorflow.keras.preprocessing.image import ImageDataGenerator


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

def load_data_for_evaluation():
    """
    This function loads test data from the local 'data/test' folder
    and returns a generator to be used for evaluating the model.
    """
    val_datagen = ImageDataGenerator(rescale=1./255)

    val_generator = val_datagen.flow_from_directory(
        "data/test",               # Folder containing test images
        target_size=(224, 224),    # Resize images to match input size of the model
        batch_size=32,
        class_mode="categorical"   # Assuming multi-class classification
    )

    return val_generator
