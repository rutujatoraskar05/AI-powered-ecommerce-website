from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.db import get_db

from services.analytics_service import (
    total_revenue,
    total_orders,
    top_products,
    top_categories
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/revenue")
def revenue(
    db: Session = Depends(get_db)
):
    return total_revenue(db)


@router.get("/orders")
def orders(
    db: Session = Depends(get_db)
):
    return total_orders(db)


@router.get("/top-products")
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
        .all()
    )

    return [
        {
            "product_name": row.product_name,
            "sold": int(row.sold)
        }
        for row in result
    ]
@router.get("/top-categories")
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
        .all()
    )

    return [
        {
            "category_name": row.category_name,
            "sold": int(row.sold)
        }
        for row in result
    ]