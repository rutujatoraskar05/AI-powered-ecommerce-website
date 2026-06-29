from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from database.base import Base


class Review(Base):

    __tablename__ = "reviews"

    review_id = Column(
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

    rating = Column(Integer)

    comment = Column(String)