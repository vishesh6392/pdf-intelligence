import boto3
import os
from io import BytesIO
from dotenv import load_dotenv
load_dotenv()

S3_BUCKET = "teacher-agent-pdf-vishesh"
S3_REGION = "us-east-1"

s3 = boto3.client(
    "s3",
    region_name=S3_REGION
)

def upload_pdf(file_obj, s3_key: str):
    s3.upload_fileobj(
        file_obj,
        S3_BUCKET,
        s3_key,
        ExtraArgs={
            "ContentType": "application/pdf"
        }
    )

def download_pdf(s3_key:str)-> BytesIO:
    buffer= BytesIO()
    s3.download_fileobj(
        Bucket=S3_BUCKET,
        Key=s3_key,
        Fileobj=buffer
    )
    buffer.seek(0)
    return buffer

def upload_file(local_path: str, s3_key: str):
    s3.upload_file(
        local_path,
        S3_BUCKET,
        s3_key
    )

def download_file(s3_key: str, local_path: str):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3.download_file(
        S3_BUCKET,
        s3_key,
        local_path
    )

        

