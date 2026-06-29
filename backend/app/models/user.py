from sqlalchemy import Column, Integer, String
from database.base import Base

class User(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))

    email = Column(String(100), unique=True)

    password = Column(String(255))

    mobile = Column(String(20))

    role = Column(String(20), default="user")