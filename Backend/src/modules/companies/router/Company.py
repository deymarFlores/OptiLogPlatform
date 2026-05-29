from fastapi import APIRouter
from src.modules.copanies.schemas.CompanySchema import CompanieSchema
from src.modules.copanies.service.CompanyService import CompanyService

router = APIRouter(prefix="/api/companies", tags=["companies"])
service = CompanyService()


@router.post("/")
async def create_company(user_id: str, data: CompanieSchema):
    return service.create(user_id, data)


@router.get("/user/{user_id}")
async def get_user_companies(user_id: str):
    return service.get_by_user(user_id)


@router.get("/{company_id}")
async def get_company(company_id: str):
    return service.get_by_id(company_id)


@router.put("/{company_id}")
async def update_company(company_id: str, data: CompanieSchema):
    return service.update(company_id, data)


@router.delete("/{company_id}")
async def delete_company(company_id: str):
    return service.delete(company_id)
