class DataIngestionArtifact:
    def __init__(self, local_file_path):
        self.local_file_path = local_file_path

from dataclasses import dataclass

@dataclass
class DataValidationArtifact:
    validation_status: bool
    report_file_path: str
