from pydantic import BaseModel


class LocationStockSchema(BaseModel):
    location_id: str
    type_material_id: str
    stock: int


class UpdateLocationStockSchema(BaseModel):
    stock: int


class LocationStockResponseSchema(BaseModel):
    id: str
    location_id: str
    type_material_id: str
    material_name: str
    stock: int
    units: str
    price: float
