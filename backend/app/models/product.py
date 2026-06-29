from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from database.base import Base

class Product(Base):

    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String(255))

    brand = Column(String(100))

    description = Column(Text)

    price = Column(Float)

    stock = Column(Integer)

    image_url = Column(Text)

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id")
    )