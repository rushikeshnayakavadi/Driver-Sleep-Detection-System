import boto3

s3 = boto3.client("s3")
bucket_name = "driver-sleep-detection-data"

response = s3.list_objects_v2(Bucket=bucket_name)
if "Contents" in response:
    print(f"✅ Found {len(response['Contents'])} files in S3 bucket: {bucket_name}")
    for obj in response["Contents"][:5]:  # Print first 5 files
        print(f"📂 {obj['Key']}")
else:
    print(f"⚠️ No files found in bucket: {bucket_name}")
