from pydantic import BaseModel
from datetime import datetime


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total: float
    payment_status: str
    order_status: str
    timestamp: datetime
    items: list[OrderItemResponse] = []

    class Config:
        from_attributes = True