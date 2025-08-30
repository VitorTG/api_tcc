from controllers.base_controller import BaseController
from repositories import UserRepository
from utils.context import Context
from errors import UserAlreadyExists, InvalidCredentials
import hashlib
import os
import base64
from datetime import datetime, timedelta
import jwt
from constants import JWT_SECRET


JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600


class UserController(BaseController):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__)
        self.user_repository = UserRepository(context)
    
    def create_user(self, user_schema):
        user_name = user_schema["user_name"]
        password = user_schema["password"]
    
        already_exist_user = self.user_repository.get_by_user_name(user_name)

        if already_exist_user is not None:
            raise UserAlreadyExists(user_name)
        
        salt = self.__generate_salt()
        password_hash = self.__hash_password(password, salt)
        user = self.user_repository.create(user_name, salt, password_hash)

        self.user_repository.commit()

        return user
    
    def validate_user(self, user_schema):
        user_name = user_schema["user_name"]
        password = user_schema["password"]

        user = self.user_repository.get_by_user_name(user_name)

        if user is None:
            raise InvalidCredentials()

        hashed_input_password = self.__hash_password(password, user.salt)

        if hashed_input_password != user.password_hash:
            raise InvalidCredentials()
        

        payload = {
            "user_name": user.user_name,
            "user_key": user.user_key,
            "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token
    

    def __generate_salt(self, length=16):
        return base64.b64encode(os.urandom(length)).decode()


    def __hash_password(self, password: str, salt: str) -> str:
        return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

