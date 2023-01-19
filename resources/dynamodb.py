import boto3

AWS_DEFAULT_REGION = "us-east-2"


def create_ddb_instance():
    resource = boto3.resource(
        service_name="dynamodb",
        region_name=AWS_DEFAULT_REGION,
        aws_access_key_id='AKIA3PB7FSYDN2KZWNA2',
        aws_secret_access_key='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',
    )
    # ddb_exceptions = dynamodb_client.exceptions
    return resource
