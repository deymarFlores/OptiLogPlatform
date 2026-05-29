from fastapi import APIRouter, Depends
from src.modules.typeLocation.schemas.TypeLocationSchemas import TypeLocationSchema
from src.modules.typeLocation.service.TypeLocationService import TypeLocationService

router = APIRouter(prefix="/api/type-locations", tags=["type-locations"])
service = TypeLocationService()


@router.post("/")
async def create_type_location(company_id: str, data: TypeLocationSchema):
    return service.create(company_id, data)


@router.get("/company/{company_id}")
async def get_company_type_locations(company_id: str):
    return service.get_by_company(company_id)


@router.get("/{type_location_id}")
async def get_type_location(type_location_id: str):
    return service.get_by_id(type_location_id)


@router.put("/{type_location_id}")
async def update_type_location(type_location_id: str, data: TypeLocationSchema):
    return service.update(type_location_id, data)


@router.delete("/{type_location_id}")
async def delete_type_location(type_location_id: str):
    return service.delete(type_location_id)
