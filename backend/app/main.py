from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Database
import database.init_db
from database.base import Base
from database.db import engine

# Models
from models.user import User
from models.category import Category
from models.product import Product
from models.order import Order
from models.order_item import OrderItem

# Routers
from routers.auth import router as auth_router
from routers.category import router as category_router
from routers.product import router as product_router
from routers.cart import router as cart_router
from routers.order import router as order_router
from routers.wishlist import router as wishlist_router
from routers.admin import router as admin_router
from routers.review import router as review_router
from routers.analytics import router as analytics_router
from routers.payment import router as payment_router

app = FastAPI(
    title="Watch Store Only"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Tables
Base.metadata.create_all(bind=engine)

# Home Route
@app.get("/")
def home():
    return {
        "message": "Watch Store Only Backend Running Successfully"
    }

# Register Routers
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(wishlist_router)
app.include_router(admin_router)
app.include_router(review_router)
app.include_router(analytics_router)
app.include_router(payment_router)

from routers.chat_router import router as chat_router
app.include_router(chat_router)
