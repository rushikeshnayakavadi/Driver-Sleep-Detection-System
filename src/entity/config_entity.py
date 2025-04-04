from dataclasses import dataclass
import os

class DataIngestionConfig:
    def __init__(self, bucket_name="driver-sleep-detection-data", local_data_path="data"):
        self.bucket_name = bucket_name
        self.local_data_path = local_data_path  # Folder to save data
        os.makedirs(self.local_data_path, exist_ok=True)  # Ensure directory exists

@dataclass
class DataValidationConfig:
    train_dir: str  # Add this
    test_dir: str   # Add this
    schema_file_path: str
    report_file_path: str

@dataclass
class DataTransformationConfig:
    target_size: tuple 
    normalization_mean: list  
    normalization_std: list  
    transformed_data_dir: str  

@dataclass
class ModelTrainerConfig:
    model_save_path: str
    learning_rate: float
    batch_size: int
    epochs: int 
    image_size: tuple = (224, 224)

