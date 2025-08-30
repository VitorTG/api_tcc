import os
import boto3

def load_parameter(var_name: str):
    if os.environ.get("APP_ENV") == "local":
        parameter_format = var_name.upper().replace("-", "_")
        return os.environ.get(parameter_format)
    else:
        try:
            ssm = boto3.client("ssm", region_name=os.getenv("AWS_REGION", "us-east-1"))
            parameter_format = var_name.lower().replace("_", "-")
            response = ssm.get_parameter(Name=parameter_format, WithDecryption=True)
            return response["Parameter"]["Value"]
        except Exception as e:
            raise ValueError(f"Error fetching parameter {parameter_format}: {e}")

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
APP_ENV = os.environ.get("APP_ENV", "local")

SECRETS_MANAGER_ENDPOINT = load_parameter("SECRETS_MANAGER_ENDPOINT")

DB_NAME = load_parameter("API_TCC_DB_NAME")
DB_PASSWORD_SECRET_NAME = load_parameter("API_TCC_DB_PASSWORD_SECRET_NAME")

JWT_SECRET = load_parameter("JWT_SECRET")

BYPASS_ENDPOINTS = ["/ufop_api/health_check", "/ufop_api/"]

SERVICE_NAME = os.environ.get("SERVICE_NAME", "weather-api")

SERVICE_ROOT = os.path.abspath(os.path.dirname(__file__))
SCHEMA_PATH = SERVICE_ROOT + "/schemas/"

GIT_COMMIT = "$$GIT_COMMIT"
GIT_BRANCH = "$$GIT_BRANCH"

WEATHER_API_KEY = load_parameter("WEATHER_API_KEY")

