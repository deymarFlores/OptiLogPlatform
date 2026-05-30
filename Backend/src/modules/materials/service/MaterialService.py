from src.core.database import db
from src.modules.materials.schemas.MaterialSchema import MaterialSchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class MaterialService:
    def __init__(self):
        self.collection = db["materials"]

    def create(self, company_id: str, data: MaterialSchema):
        try:
            material = {
                "company_id": ObjectId(company_id),
                "name": data.name,
                "stock": data.stock
            }
            result = self.collection.insert_one(material)
            return {
                "id": str(result.inserted_id),
                "company_id": company_id,
                "name": data.name,
                "stock": data.stock
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear material: {str(e)}")

    def get_by_company(self, company_id: str):
        try:
            materials = list(self.collection.find({"company_id": ObjectId(company_id)}))
            return [
                {
                    "id": str(m["_id"]),
                    "name": m["name"],
                    "stock": m["stock"]
                }
                for m in materials
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener materiales: {str(e)}")

    def get_by_id(self, material_id: str):
        try:
            material = self.collection.find_one({"_id": ObjectId(material_id)})
            if not material:
                raise HTTPException(status_code=404, detail="Material no encontrado")
            return {
                "id": str(material["_id"]),
                "company_id": str(material["company_id"]),
                "name": material["name"],
                "stock": material["stock"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener material: {str(e)}")

    def update(self, material_id: str, data: MaterialSchema):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(material_id)},
                {"$set": {
                    "name": data.name,
                    "stock": data.stock
                }}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Material no encontrado")
            return {"message": "Material actualizado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar material: {str(e)}")

    def delete(self, material_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(material_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Material no encontrado")
            return {"message": "Material eliminado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar material: {str(e)}")
