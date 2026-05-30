from fastapi import APIRouter
from src.modules.materials.schemas.MaterialSchema import MaterialSchema
from src.modules.materials.service.MaterialService import MaterialService

router = APIRouter(prefix="/api/materials", tags=["materials"])
service = MaterialService()


@router.post("/")
async def create_material(company_id: str, data: MaterialSchema):
    return service.create(company_id, data)


@router.get("/company/{company_id}")
async def get_company_materials(company_id: str):
    return service.get_by_company(company_id)


@router.get("/{material_id}")
async def get_material(material_id: str):
    return service.get_by_id(material_id)


@router.put("/{material_id}")
async def update_material(material_id: str, data: MaterialSchema):
    return service.update(material_id, data)


@router.delete("/{material_id}")
async def delete_material(material_id: str):
    return service.delete(material_id)
