from fastapi import APIRouter
from fastapi import Depends
from services.order_service import update_order_status
from sqlalchemy.orm import Session

from database.db import get_db

from dependencies.admin import get_admin_user

from services.admin_service import (
    dashboard_stats,
    get_all_users,
    get_all_orders
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    return dashboard_stats(db)


@router.get("/users")
def users(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    return get_all_users(db)


@router.get("/orders")
def orders(
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    return get_all_orders(db)

@router.put("/order-status/{order_id}")
def change_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):

    order = update_order_status(
        db,
        order_id,
        status
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order Not Found"
        )

    return {
        "message": "Status Updated",
        "status": order.status
    }