from fastapi import APIRouter

from schemas.payment import PaymentRequest
from services.payment_service import create_payment

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)

@router.post("/create-order")
def payment_order(
    payment: PaymentRequest
):

    return create_payment(
        payment.amount
    )