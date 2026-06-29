from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from database.base import Base


class Cart(Base):
    __tablename__ = "carts"

    cart_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))