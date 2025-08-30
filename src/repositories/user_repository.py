from utils.context import Context
from models import User
import uuid

from repositories import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, context: Context) -> None:
        super().__init__(context=context, class_name=__name__)

    def create(
        self,
        user_name,
        salt,
        password_hash
    ) -> User:
        user = User()
        user.user_key = str(uuid.uuid4())
        user.user_name = user_name
        user.salt = salt
        user.password_hash = password_hash

        self.add(user)
        return user
    

    def get_by_user_name(
        self,
        user_name: str,
    ) -> User:
        response = self.query(User).filter(User.user_name == user_name).first()

        return response

