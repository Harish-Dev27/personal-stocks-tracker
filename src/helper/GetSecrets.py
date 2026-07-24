import boto3
from botocore.exceptions import ClientError

class GetSecrets:

    def __init__(self):
        pass

    @staticmethod
    def get_secret():

        secret_name = "open-ai-api-key"
        region_name = "ap-south-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        secret = get_secret_value_response['SecretString']
        return secret
