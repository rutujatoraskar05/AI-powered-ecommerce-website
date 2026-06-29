from sqlalchemy import Column, Integer, ForeignKey
from database.base import Base

class Wishlist(Base):

    __tablename__ = "wishlist"

    wishlist_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id")
    )