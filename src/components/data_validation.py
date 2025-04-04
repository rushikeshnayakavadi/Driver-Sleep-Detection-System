import os
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact
from src.utils.main_utils import save_json

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_folders(self) -> bool:
        """Check if train and test folders contain the required subdirectories."""
        required_subfolders = {"Closed", "Open", "yawn", "no_yawn"}  # Updated to match actual folder names

        # Check Train Folder
        if not os.path.exists(self.config.train_dir):
            print(f"Error: Train directory '{self.config.train_dir}' not found.")
            return False

        train_subfolders = set(os.listdir(self.config.train_dir))
        if not required_subfolders.issubset(train_subfolders):
            print(f"Error: Train directory missing subfolders. Found: {train_subfolders}")
            return False

        # Check Test Folder
        if not os.path.exists(self.config.test_dir):
            print(f"Error: Test directory '{self.config.test_dir}' not found.")
            return False

        test_subfolders = set(os.listdir(self.config.test_dir))
        if not required_subfolders.issubset(test_subfolders):
            print(f"Error: Test directory missing subfolders. Found: {test_subfolders}")
            return False

        return True

    def validate_images(self) -> bool:
        """Check if each category contains at least one image file."""
        required_subfolders = {"Closed", "Open", "yawn", "no_yawn"}


        for folder in [self.config.train_dir, self.config.test_dir]:
            for subfolder in required_subfolders:
                subfolder_path = os.path.join(folder, subfolder)
                if not os.listdir(subfolder_path):  # Check if folder is empty
                    print(f"Error: No images found in '{subfolder_path}'")
                    return False
        
        return True

    def initiate_data_validation(self) -> DataValidationArtifact:
        """Perform data validation and generate a report."""
        folder_validation = self.validate_folders()
        image_validation = self.validate_images()
        validation_status = folder_validation and image_validation

        # Save validation report
        report_data = {"validation_status": validation_status}
        save_json(self.config.report_file_path, report_data)

        print(f"Validation Status: {validation_status}")  # Debugging Output

        return DataValidationArtifact(
            validation_status=validation_status,
            report_file_path=self.config.report_file_path
        )

if __name__ == "__main__":
    print("Starting Data Validation...")  # Debugging Output

    validation_config = DataValidationConfig(
    train_dir="data/train",
    test_dir="data/test",
    schema_file_path="config/schema.yaml",  # Path to your schema file
    report_file_path="reports/data_validation.json"
)


    data_validator = DataValidation(validation_config)
    validation_result = data_validator.initiate_data_validation()

    print("Data Validation Complete:", validation_result.validation_status)
