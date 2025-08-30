from sqlalchemy import Column, Integer, String
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_key = Column(String(36))
    user_name = Column(String(255))
    salt = Column(String(255))
    password_hash = Column(String(255))