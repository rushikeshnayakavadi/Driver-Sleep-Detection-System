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
