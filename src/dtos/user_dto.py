from models import User
from typing import List
from copy import deepcopy


class UserDTO:
    @staticmethod
    def obj_to_dict(user: User) -> dict:
        dto = {
            "user_key": user.user_key,
            "user_name": user.user_name
        }
        return dto

    @staticmethod
    def list_obj_to_list_dict(user_list: List[User]) -> List[dict]:
        return [UserDTO.obj_to_dict(user) for user in user_list]

    @staticmethod
    def only_obj_key(user: User) -> dict:
        return {"user_key": user.user_key}
    
    @staticmethod
    def login_success(token: str):
        return {
            "message": "Login successful",
            "access_token": token
        }
