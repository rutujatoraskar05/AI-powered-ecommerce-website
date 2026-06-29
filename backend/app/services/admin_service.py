from models.user import User
from models.product import Product
from models.order import Order
from sqlalchemy import func


def dashboard_stats(db):

    total_users = db.query(User).count()

    total_products = db.query(Product).count()

    total_orders = db.query(Order).count()

    revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": revenue or 0
    }

def get_all_users(db):

    users = db.query(User).all()

    return users

def get_all_orders(db):

    orders = db.query(Order).all()

    return orders