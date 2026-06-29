from models.user import User
from models.category import Category
from models.product import Product
from models.cart import Cart
from models.cart_item import CartItem
from models.order import Order
from models.order_item import OrderItem
from models.wishlist import Wishlist

from database.base import Base
from database.db import engine

Base.metadata.create_all(bind=engine)