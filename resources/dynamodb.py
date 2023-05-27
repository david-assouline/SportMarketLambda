import os

import boto3

AWS_DEFAULT_REGION = "us-east-2"


# def create_ddb_instance():
#     resource = boto3.resource(
#         service_name="dynamodb",
#         region_name=AWS_DEFAULT_REGION,
#         aws_access_key_id='AKIA3PB7FSYDN2KZWNA2',
#         aws_secret_access_key='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',
#     )
#     # ddb_exceptions = dynamodb_client.exceptions
#     return resource

def create_ddb_instance():
    sts_client = boto3.client('sts')

    try:
        # Specify the ARN of the IAM role you want to assume
        role_to_assume_arn = os.getenv("STS_ARN")

        # Assume the IAM role
        response = sts_client.assume_role(
            RoleArn=role_to_assume_arn,
            RoleSessionName='AssumedRoleSession'
        )

        # Extract the temporary credentials
        assumed_role_credentials = response['Credentials']

        # Use the assumed role credentials for further AWS operations
        # For example, create an S3 client with the assumed role credentials
        dynamodb = boto3.resource(
            'dynamodb',
            region_name=AWS_DEFAULT_REGION,
            aws_access_key_id=assumed_role_credentials['AccessKeyId'],
            aws_secret_access_key=assumed_role_credentials['SecretAccessKey'],
            aws_session_token=assumed_role_credentials['SessionToken']
        )

        return dynamodb

    except Exception as e:
        print('Error assuming IAM role:', str(e))
