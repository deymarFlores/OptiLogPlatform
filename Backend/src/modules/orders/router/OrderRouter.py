from fastapi import APIRouter
from src.modules.orders.schemas.OrderSchema import OrderSchema
from src.modules.orders.service.OrderService import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])
service = OrderService()


@router.post("/")
async def create_order(data: OrderSchema):
    """Crear una nueva orden/pedido del cliente"""
    return service.create(data)


@router.get("/user/{user_id}")
async def get_user_orders(user_id: str):
    """Obtener todas las órdenes de un usuario (cliente)"""
    return service.get_by_user(user_id)


@router.get("/company/{company_id}")
async def get_company_orders(company_id: str):
    """Obtener todas las órdenes recibidas por una empresa"""
    return service.get_by_company(company_id)


@router.get("/{order_id}")
async def get_order(order_id: str):
    """Obtener una orden por ID"""
    return service.get_by_id(order_id)
