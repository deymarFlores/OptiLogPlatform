from fastapi import APIRouter
from src.modules.typeMaterials.schemas.TypeMaterials import TypeMaterialSchema
from src.modules.typeMaterials.service.TypeMaterialService import TypeMaterialService

router = APIRouter(prefix="/api/type-materials", tags=["type-materials"])
service = TypeMaterialService()


@router.post("/")
async def create_type_material(company_id: str, data: TypeMaterialSchema):
    return service.create(company_id, data)


@router.get("/company/{company_id}")
async def get_company_type_materials(company_id: str):
    return service.get_by_company(company_id)


@router.get("/{type_material_id}")
async def get_type_material(type_material_id: str):
    return service.get_by_id(type_material_id)


@router.put("/{type_material_id}")
async def update_type_material(type_material_id: str, data: TypeMaterialSchema):
    return service.update(type_material_id, data)


@router.delete("/{type_material_id}")
async def delete_type_material(type_material_id: str):
    return service.delete(type_material_id)
