from pathlib import Path
from os import path, environ
import json
from tests.utils.localstack import LocalStack

root = Path.cwd()
if not environ.get("APP_ENV") or environ.get("APP_ENV") == "local":
    from dotenv import load_dotenv

    dot_env_path = path.join(str(root), "local.env")
    load_dotenv(dot_env_path)
    if environ.get("SERVER_LOCALHOST") is None:
        environ["SERVER_LOCALHOST"] = "0.0.0.0"

db_password_secret_name = environ.get("API_TCC_DB_PASSWORD_SECRET_NAME")
LocalStack.create_secret(
    db_password_secret_name,
    json.dumps({"password": "my_pwd", "username": "my_user", "host": "db", "port": 5432}),
)

internal_token_secret_name = environ.get("API_TCC_INTERNAL_TOKEN_SECRET_NAME")
LocalStack.create_secret(internal_token_secret_name, "default_token")
