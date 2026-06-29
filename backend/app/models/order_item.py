from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric

from database.base import Base


class OrderItem(Base):

    __tablename__ = "order_items"


    order_item_id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    order_id = Column(
        Integer,
        ForeignKey("orders.order_id")
    )


    product_id = Column(
        Integer,
        ForeignKey("products.product_id")
    )


    quantity = Column(
        Integer
    )


    price = Column(
        Numeric(10,2)
    )