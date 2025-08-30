import boto3
from constants import APP_ENV, SECRETS_MANAGER_ENDPOINT, AWS_REGION

from utils.logger import LogHandler

logger = LogHandler().get_logger(__name__)


class SecretsManagerConnector:
    @staticmethod
    def get_client():
        if APP_ENV.upper() == "LOCAL":
            secrets_manager = boto3.client(
                service_name="secretsmanager",
                aws_access_key_id="aaa",
                aws_secret_access_key="bbb",
                region_name="us-east-1",
                endpoint_url="http://localstack:4566/",
            )
        else:
            secrets_manager = boto3.client(
                "secretsmanager",
                region_name=AWS_REGION,
                endpoint_url=SECRETS_MANAGER_ENDPOINT,
            )
        return secrets_manager

    @staticmethod
    def get_secret_by_name(secret_name):
        manager = SecretsManagerConnector.get_client()
        resp = manager.get_secret_value(SecretId=secret_name)
        return {"secret_string_value": resp["SecretString"]}
