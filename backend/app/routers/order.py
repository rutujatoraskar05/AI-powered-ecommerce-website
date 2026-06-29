from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.db import get_db

from dependencies.auth import get_current_user

from services.order_service import place_order
from services.order_service import get_user_orders
from services.order_service import get_order_by_id
from services.order_service import cancel_order

from services.email_service import send_order_email

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/place")
async def create_order(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    order = place_order(
        db,
        current_user.user_id
    )

    if order is None:
        raise HTTPException(
            status_code=400,
            detail="Cart Empty"
        )

    if isinstance(order, dict):
        raise HTTPException(
            status_code=400,
            detail=order["error"]
        )

    # Send Email
    await send_order_email(
        current_user.email,
        order.order_id,
        order.total_amount
    )

    return {
        "message": "Order Placed Successfully",
        "order_id": order.order_id,
        "total_amount": order.total_amount
    }


@router.get("/")
def all_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_user_orders(
        db,
        current_user.user_id
    )


@router.get("/{order_id}")
def single_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    order = get_order_by_id(
        db,
        order_id,
        current_user.user_id
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order Not Found"
        )

    return order


@router.put("/cancel/{order_id}")
def cancel_user_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = cancel_order(
        db,
        order_id,
        current_user.user_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Order Not Found"
        )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Order Already Cancelled"
        )

    return {
        "message": "Order Cancelled Successfully"
    }

from fastapi_mail import FastMail
from fastapi_mail import MessageSchema

from utils.email_config import conf


async def send_order_email(
    email,
    order_id,
    amount
):

    message = MessageSchema(
        subject="Order Confirmation",
        recipients=[email],
        body=f"""
Thank you for your order.

Order ID: {order_id}
Total Amount: ₹{amount}

Your order has been placed successfully.
        """,
        subtype="plain"
    )

    fm = FastMail(conf)

    await fm.send_message(message)