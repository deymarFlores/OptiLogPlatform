from fastapi import APIRouter
from src.modules.orders.schemas.OrderSchema import OrderSchema
from src.modules.orders.service.OrderService import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])
service = OrderService()


@router.post("/")
async def create_order(data: OrderSchema):
    return service.create(data)


@router.get("/user/{user_id}")
async def get_user_orders(user_id: str):
    return service.get_by_user(user_id)


@router.get("/company/{company_id}")
async def get_company_orders(company_id: str):
    return service.get_by_company(company_id)


@router.get("/{order_id}")
async def get_order(order_id: str):
    return service.get_by_id(order_id)
