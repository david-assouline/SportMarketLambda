import boto3
AWS_DEFAULT_REGION = "us-east-2"

def create_ddb_instance():
    client = boto3.resource(
        service_name="dynamodb",
        region_name="us-east-2",
        aws_access_key_id="AKIA3PB7FSYDHR53Z356",
        aws_secret_access_key="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",
    )
    # ddb_exceptions = dynamodb_client.exceptions
    return client

