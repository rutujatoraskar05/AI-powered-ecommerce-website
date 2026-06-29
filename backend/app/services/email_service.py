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