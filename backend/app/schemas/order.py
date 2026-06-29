from pydantic import BaseModel


class OrderResponse(BaseModel):

    order_id: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True