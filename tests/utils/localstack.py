import boto3
from os import environ


class LocalStack(object):
    @staticmethod
    def get_client(service_name):
        boto_client = boto3.client(
            service_name=service_name,
            aws_access_key_id="aaa",
            aws_secret_access_key="bbb",
            region_name="us-east-1",
            endpoint_url=f'http://{environ["SERVER_LOCALHOST"]}:4566/',
        )

        return boto_client

    @staticmethod
    def create_secret(secret_name, secret_value):
        secrets_client = LocalStack.get_client("secretsmanager")
        secrets_client.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
        secrets_client.create_secret(Name=secret_name, SecretString=secret_value)
