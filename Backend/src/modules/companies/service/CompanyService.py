from src.core.database import db
from src.modules.companies.schemas.CompanySchema import CompanieSchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class CompanyService:
    def __init__(self):
        self.collection = db["companies"]

    def create(self, user_id: str, data: CompanieSchema):
        try:
            company = {
                "user_id": ObjectId(user_id),
                "name": data.name,
                "address": data.address,
                "phone": data.phone
            }
            result = self.collection.insert_one(company)
            return {
                "id": str(result.inserted_id),
                "user_id": user_id,
                "name": data.name,
                "address": data.address,
                "phone": data.phone
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear empresa: {str(e)}")

    def get_by_user(self, user_id: str):
        try:
            companies = list(self.collection.find({"user_id": ObjectId(user_id)}))
            return [
                {
                    "id": str(c["_id"]),
                    "name": c["name"],
                    "address": c["address"],
                    "phone": c["phone"]
                }
                for c in companies
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener empresas: {str(e)}")

    def get_by_id(self, company_id: str):
        try:
            company = self.collection.find_one({"_id": ObjectId(company_id)})
            if not company:
                raise HTTPException(status_code=404, detail="Empresa no encontrada")
            return {
                "id": str(company["_id"]),
                "user_id": str(company["user_id"]),
                "name": company["name"],
                "address": company["address"],
                "phone": company["phone"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener empresa: {str(e)}")

    def update(self, company_id: str, data: CompanieSchema):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$set": {
                    "name": data.name,
                    "address": data.address,
                    "phone": data.phone
                }}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Empresa no encontrada")
            return {"message": "Empresa actualizada"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar empresa: {str(e)}")

    def delete(self, company_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(company_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Empresa no encontrada")
            return {"message": "Empresa eliminada"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar empresa: {str(e)}")
