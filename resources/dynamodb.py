import boto3
import os

from dotenv import load_dotenv
load_dotenv()

AWS_DEFAULT_REGION = "us-east-2"


def create_ddb_instance():
    resource = boto3.resource(
        service_name="dynamodb",
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    )
    # ddb_exceptions = dynamodb_client.exceptions
    return resource
