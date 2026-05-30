from pydantic import BaseModel
from typing import Optional


class OrderSchema(BaseModel):
    """Schema para crear un pedido/orden"""
    user_id: str  # ID del cliente que hace el pedido
    company_id: str  # ID de la empresa proveedora
    product_id: str  # ID del producto/material
    product_name: str  # Nombre del producto
    quantity: int  # Cantidad ordenada
    price: float  # Precio unitario
    delivery_lat: float  # Latitud de entrega
    delivery_lng: float  # Longitud de entrega
    company_name: Optional[str] = None  # Nombre de la empresa


class OrderResponseSchema(BaseModel):
    """Schema para respuesta de pedido"""
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
