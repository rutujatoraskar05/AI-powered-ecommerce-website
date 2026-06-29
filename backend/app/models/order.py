from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import DateTime, Numeric, String
from sqlalchemy.sql import func

from database.base import Base


class Order(Base):

    __tablename__ = "orders"


    order_id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )


    order_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    total_amount = Column(
        Numeric(10,2)
    )


    status = Column(
        String(50),
        default="Placed"
    )


    tracking_id = Column(
        String(100),
        nullable=True
    )


    expected_delivery = Column(
        String(100),
        nullable=True
    )


    customer_name = Column(
        String(100),
        nullable=True
    )


    address = Column(
        String(255),
        nullable=True
    )


    payment_method = Column(
    String(50),
    nullable=True
)