import boto3
import os
import logging
from src.constants import MODEL_BUCKET_NAME, MODEL_PUSHER_S3_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class S3ModelResolver:
    def __init__(self):
        self.s3 = boto3.client("s3")

    def get_latest_model_path(self):
        try:
            logging.info("Checking for existing models in S3 bucket...")
            response = self.s3.list_objects_v2(Bucket=MODEL_BUCKET_NAME, Prefix=MODEL_PUSHER_S3_KEY)

            if 'Contents' not in response:
                logging.info("No models found in S3.")
                return None

            models = sorted([obj['Key'] for obj in response['Contents'] if obj['Key'].endswith(".h5")])
            if not models:
                logging.info("No model files with .h5 extension found.")
                return None

            latest_model_key = models[-1]
            local_path = os.path.join("artifacts", "latest_model.h5")
            self.s3.download_file(MODEL_BUCKET_NAME, latest_model_key, local_path)
            logging.info(f"Downloaded latest model from S3: {latest_model_key}")
            return local_path

        except Exception as e:
            logging.error(f"Error while fetching model from S3: {str(e)}")
            return None

    def push_model_to_s3(self, local_model_path):
        try:
            model_name = os.path.basename(local_model_path)
            key = f"{MODEL_PUSHER_S3_KEY}/{model_name}"
            self.s3.upload_file(local_model_path, MODEL_BUCKET_NAME, key)
            logging.info(f"Uploaded model to S3: {key}")
        except Exception as e:
            logging.error(f"Error while uploading model to S3: {str(e)}")
            raise e
