import boto3
from os import environ
from .singleton import Singleton


class SecretsManager(metaclass=Singleton):
    def __init__(self) -> None:
        self.client = self.get_client("secretsmanager")

    def get_client(self, service_name):
        boto_client = boto3.client(
            service_name=service_name,
            aws_access_key_id="aaa",
            aws_secret_access_key="bbb",
            region_name="us-east-1",
            endpoint_url=f'http://{environ["SERVER_LOCALHOST"]}:4566/',
        )

        return boto_client

    def create_secret(self, secret_name, secret_value):
        self.client.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
        self.client.create_secret(Name=secret_name, SecretString=secret_value)
