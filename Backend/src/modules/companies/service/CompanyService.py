from src.core.database import db
from src.modules.companies.schemas.CompanySchema import CompanieSchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class CompanyService:
    def __init__(self):
        self.collection = db["companies"]
        self._create_indexes()

    def _create_indexes(self):
        try:
            self.collection.create_index([("name", 1)], unique=True)
        except Exception:
            pass

    def create(self, user_id: str, data: CompanieSchema):
        try:
            existing_company = self.collection.find_one({
                "name": data.name
            })
            
            if existing_company:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Ya existe una empresa con el nombre '{data.name}'"
                )
            
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
        except HTTPException:
            raise
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
            company = self.collection.find_one({"_id": ObjectId(company_id)})
            if not company:
                raise HTTPException(status_code=404, detail="Empresa no encontrada")
            
            if company["name"] != data.name:
                existing_company = self.collection.find_one({
                    "name": data.name,
                    "_id": {"$ne": ObjectId(company_id)}
                })
                
                if existing_company:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Ya existe una empresa con el nombre '{data.name}'"
                    )
            
            result = self.collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$set": {
                    "name": data.name,
                    "address": data.address,
                    "phone": data.phone
                }}
            )
            return {"message": "Empresa actualizada"}
        except HTTPException:
            raise
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