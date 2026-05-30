from fastapi import APIRouter
from src.modules.materials.schemas.LocationStockSchema import LocationStockSchema, UpdateLocationStockSchema
from src.modules.materials.service.LocationStockService import LocationStockService

router = APIRouter(prefix="/api/location-stocks", tags=["location-stocks"])
service = LocationStockService()


@router.post("/")
async def create_location_stock(data: LocationStockSchema):
    return service.create(data)


@router.get("/location/{location_id}")
async def get_location_stocks(location_id: str):
    return service.get_by_location(location_id)


@router.get("/{stock_id}")
async def get_location_stock(stock_id: str):
    return service.get_by_id(stock_id)


@router.put("/{stock_id}")
async def update_location_stock(stock_id: str, data: UpdateLocationStockSchema):
    return service.update_stock(stock_id, data)


@router.post("/{stock_id}/add")
async def add_to_stock(stock_id: str, quantity: int):
    return service.add_stock(stock_id, quantity)


@router.post("/{stock_id}/subtract")
async def subtract_from_stock(stock_id: str, quantity: int):
    return service.subtract_stock(stock_id, quantity)


@router.delete("/{stock_id}")
async def delete_location_stock(stock_id: str):
    return service.delete(stock_id)
