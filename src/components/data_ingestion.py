import os
import boto3
import pandas as pd
import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.s3_client = boto3.client("s3")
    
    def download_data_from_s3(self, s3_folder="train"):
        """Download data from S3 and maintain folder structure."""
        local_folder = os.path.join(self.config.local_data_path, s3_folder)
        os.makedirs(local_folder, exist_ok=True)  # ✅ Ensure `train/` or `test/` exists

        response = self.s3_client.list_objects_v2(Bucket=self.config.bucket_name, Prefix=s3_folder)
        if "Contents" not in response:
            logging.warning(f"No files found in S3: {s3_folder}")
            return None

        for obj in response["Contents"]:
            s3_file_path = obj["Key"]  # Example: 'train/Closed/image1.jpg'
            
            # ✅ Extract subfolder name (Closed, No_Yawn, Open, Yawn)
            subfolder_name = os.path.dirname(s3_file_path).split("/")[-1]  
            
            # ✅ Create local subfolder (train/Closed, train/Open, etc.)
            subfolder_path = os.path.join(local_folder, subfolder_name)
            os.makedirs(subfolder_path, exist_ok=True)

            # ✅ Save file inside correct subfolder
            local_file_path = os.path.join(subfolder_path, os.path.basename(s3_file_path))

            # ✅ Download file
            self.s3_client.download_file(self.config.bucket_name, s3_file_path, local_file_path)
            logging.info(f"Downloaded {s3_file_path} → {local_file_path}")

        return local_folder
    
    def transform_data(self, folder):
        """Convert images metadata into a DataFrame."""
        logging.info(f"📂 Transforming data in {folder}")
        images = []
        
        for root, _, files in os.walk(folder):
            for file in files:
                images.append({"image_path": os.path.join(root, file), "label": os.path.basename(root)})

        df = pd.DataFrame(images)
        logging.info(f"📊 Data transformed: {df.shape[0]} rows")
        return df

    def initiate_data_ingestion(self):
        """Run the full data ingestion process."""
        logging.info("🚀 Starting data ingestion...")

        train_folder = self.download_data_from_s3("train")
        test_folder = self.download_data_from_s3("test")

        if train_folder and test_folder:
            logging.info("🔄 Transforming train & test data into DataFrame...")
            train_df = self.transform_data(train_folder)
            test_df = self.transform_data(test_folder)

            logging.info("🎉 Data Ingestion completed!")
            return DataIngestionArtifact(local_file_path=train_folder), train_df, test_df
        else:
            logging.error("❌ Data Ingestion failed due to missing files.")
            return None
