from pydantic import BaseModel
from typing import Optional


class OrderSchema(BaseModel):
    user_id: str
    company_id: str
    product_id: str
    product_name: str
    quantity: int
    price: float
    delivery_lat: float
    delivery_lng: float
    company_name: Optional[str] = None


class OrderResponseSchema(BaseModel):
    id: str
    user_id: str
    company_id: str
    product_id: str
    product_name: str
    quantity: int
    price: float
    total_amount: float
    delivery_lat: float
    delivery_lng: float
    company_name: str
    created_at: str
