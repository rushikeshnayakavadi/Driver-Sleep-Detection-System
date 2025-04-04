from components.data_validation import DataValidation
from src.entity.config_entity import DataValidationConfig
import pandas as pd

def start_training_pipeline():
    # Load data
    df = pd.read_csv("data/train_labels.csv")  # Adjust path if needed

    # Data Validation
    validation_config = DataValidationConfig(
        schema_file_path="config/schema.yaml",
        report_file_path="reports/data_validation.json"
    )

    data_validator = DataValidation(validation_config)
    validation_result = data_validator.initiate_data_validation(df)

    if not validation_result.validation_status:
        raise Exception("Data validation failed. Check the report.")
