import pandas as pd
import boto3
import os
from io import BytesIO
from src.configuration.aws_connection import get_s3_client
from src.constants import AWS_S3_BUCKET_NAME

s3 = get_s3_client()

def read_csv_from_s3(s3_folder, file_name):
    """
    Reads a CSV file from AWS S3 and loads it into a pandas DataFrame.
    """
    try:
        obj = s3.get_object(Bucket=AWS_S3_BUCKET_NAME, Key=f"{s3_folder}/{file_name}")
        df = pd.read_csv(BytesIO(obj['Body'].read()))
        return df
    except Exception as e:
        print(f"Error fetching {file_name} from S3: {e}")
        return None
