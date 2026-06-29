from sqlalchemy import func

from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from models.category import Category


def total_revenue(db):

    revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    return {
        "total_revenue": revenue or 0
    }


def total_orders(db):

    count = db.query(
        Order
    ).count()

    return {
        "total_orders": count
    }


def top_products(db):

    result = (
        db.query(
            Product.product_name,
            func.sum(OrderItem.quantity).label("sold")
        )
        .join(
            OrderItem,
            Product.product_id == OrderItem.product_id
        )
        .group_by(
            Product.product_name
        )
        .order_by(
            func.sum(OrderItem.quantity).desc()
        )
        .all()
    )

    return result


def top_categories(db):

    result = (
        db.query(
            Category.category_name,
            func.sum(OrderItem.quantity).label("sold")
        )
        .join(
            Product,
            Category.category_id == Product.category_id
        )
        .join(
            OrderItem,
            Product.product_id == OrderItem.product_id
        )
        .group_by(
            Category.category_name
        )
        .order_by(
            func.sum(OrderItem.quantity).desc()
        )
        .all()
    )

    return result