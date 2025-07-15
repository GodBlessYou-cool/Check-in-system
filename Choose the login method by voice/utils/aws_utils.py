import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_aws_clients():
    session = boto3.Session()  # Automatically uses credentials from ~/.aws/credentials
    return {
        's3': session.client('s3'),
        'rekognition': session.client('rekognition'),
        'dynamodb': session.resource('dynamodb')
    }

def get_config():
    bucket_name = os.getenv('S3_BUCKET', 'customerimage1')  # Default fallback
    if not bucket_name:
        raise ValueError("S3_BUCKET must be set in environment variables")
        
    return {
        'bucket': bucket_name,
        'table_name': os.getenv('DYNAMODB_TABLE', 'Customers'),
        'collection_id': os.getenv('REKOGNITION_COLLECTION', 'my-users')
    }