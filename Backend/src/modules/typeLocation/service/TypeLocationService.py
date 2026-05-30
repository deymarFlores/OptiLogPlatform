from src.core.database import db
from src.modules.typeLocation.schemas.TypeLocationSchemas import TypeLocationSchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class TypeLocationService:
    def __init__(self):
        self.collection = db["type_locations"]

    def create(self, company_id: str, data: TypeLocationSchema):
        try:
            type_location = {
                "company_id": ObjectId(company_id),
                "name": data.name,
                "icon": data.icon,
                "color": data.color
            }
            result = self.collection.insert_one(type_location)
            return {
                "id": str(result.inserted_id),
                "company_id": company_id,
                "name": data.name,
                "icon": data.icon,
                "color": data.color
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear tipo de location: {str(e)}")

    def get_by_company(self, company_id: str):
        try:
            types = list(self.collection.find({"company_id": ObjectId(company_id)}))
            return [
                {
                    "id": str(t["_id"]),
                    "name": t["name"],
                    "icon": t["icon"],
                    "color": t["color"]
                }
                for t in types
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipos de location: {str(e)}")

    def get_by_id(self, type_location_id: str):
        try:
            type_location = self.collection.find_one({"_id": ObjectId(type_location_id)})
            if not type_location:
                raise HTTPException(status_code=404, detail="Tipo de location no encontrado")
            return {
                "id": str(type_location["_id"]),
                "name": type_location["name"],
                "icon": type_location["icon"],
                "color": type_location["color"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipo de location: {str(e)}")

    def update(self, type_location_id: str, data: TypeLocationSchema):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(type_location_id)},
                {"$set": {
                    "name": data.name,
                    "icon": data.icon,
                    "color": data.color
                }}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Tipo de location no encontrado")
            return {"message": "Tipo de location actualizado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar tipo de location: {str(e)}")

    def delete(self, type_location_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(type_location_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Tipo de location no encontrado")
            return {"message": "Tipo de location eliminado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar tipo de location: {str(e)}")
