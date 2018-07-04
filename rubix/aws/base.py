import os
import boto3


def get_client(service, **kwargs):
    '''
    Validates credentials and region is present.
    Returns client for the required AWS service.
    '''

    aws_access_key_id = kwargs.get('aws_access_key_id') or os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = kwargs.get('aws_secret_access_key') or os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = kwargs.get('aws_region') or os.environ.get('AWS_REGION')

    if not aws_access_key_id:
        raise ValueError(
            'aws_access_key_id is not specified. Either send it as a method argument: aws_access_key_id Or set the environment variable: AWS_ACCESS_KEY_ID')

    if not aws_secret_access_key:
        raise ValueError(
            'aws_secret_access_key is not specified. Either send it as a method argument: aws_secret_access_key Or set the environment variable: AWS_SECRET_ACCESS_KEY')

    if not aws_region:
        raise ValueError(
            'aws_region is not specified. Either send it as a method argument: aws_region Or set the environment variable: AWS_REGION')

    return boto3.client(
        service,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
