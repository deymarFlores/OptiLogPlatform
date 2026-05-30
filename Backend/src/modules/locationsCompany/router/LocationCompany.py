from fastapi import APIRouter
from src.modules.locationsCompany.schemas.LocationCompanySchema import LocationCompanySchema
from src.modules.locationsCompany.service.LocationCompanyService import LocationCompanyService

router = APIRouter(prefix="/api/locations", tags=["locations"])
service = LocationCompanyService()


@router.post("/")
async def create_location(company_id: str, data: LocationCompanySchema):
    return service.create(company_id, data)


@router.get("/company/{company_id}")
async def get_company_locations(company_id: str):
    return service.get_by_company(company_id)


@router.get("/{location_id}")
async def get_location(location_id: str):
    return service.get_by_id(location_id)


@router.put("/{location_id}")
async def update_location(location_id: str, data: LocationCompanySchema):
    return service.update(location_id, data)


@router.delete("/{location_id}")
async def delete_location(location_id: str):
    return service.delete(location_id)
