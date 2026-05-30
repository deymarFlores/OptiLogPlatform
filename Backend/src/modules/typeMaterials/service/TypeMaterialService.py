from src.core.database import db
from src.modules.typeMaterials.schemas.TypeMaterials import TypeMaterialSchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class TypeMaterialService:
    def __init__(self):
        self.collection = db["type_materials"]
        self.location_stock_collection = db["location_stock"]
        self.companies_collection = db["companies"]

    def create(self, company_id: str, data: TypeMaterialSchema):
        try:
            type_material = {
                "company_id": ObjectId(company_id),
                "name": data.name,
                "price": data.price,
                "units": data.units
            }
            result = self.collection.insert_one(type_material)
            return {
                "id": str(result.inserted_id),
                "company_id": company_id,
                "name": data.name,
                "price": data.price,
                "units": data.units
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear tipo de material: {str(e)}")

    def get_by_company(self, company_id: str):
        try:
            materials = list(self.collection.find({"company_id": ObjectId(company_id)}))
            return [
                {
                    "id": str(m["_id"]),
                    "name": m["name"],
                    "price": m["price"],
                    "units": m["units"]
                }
                for m in materials
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipos de materiales: {str(e)}")

    def get_by_id(self, type_material_id: str):
        try:
            material = self.collection.find_one({"_id": ObjectId(type_material_id)})
            if not material:
                raise HTTPException(status_code=404, detail="Tipo de material no encontrado")
            return {
                "id": str(material["_id"]),
                "name": material["name"],
                "price": material["price"],
                "units": material["units"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener tipo de material: {str(e)}")

    def update(self, type_material_id: str, data: TypeMaterialSchema):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(type_material_id)},
                {"$set": {
                    "name": data.name,
                    "price": data.price,
                    "units": data.units
                }}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Tipo de material no encontrado")
            return {"message": "Tipo de material actualizado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar tipo de material: {str(e)}")

    def delete(self, type_material_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(type_material_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Tipo de material no encontrado")
            return {"message": "Tipo de material eliminado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar tipo de material: {str(e)}")

    # NUEVO MÉTODO PARA BÚSQUEDA DE PRODUCTOS
    def search_products(self, query: str):
        try:
            materials = list(self.collection.find({
                "name": {"$regex": query, "$options": "i"}
            }))
            
            if not materials:
                return []
            
            results = []
            for material in materials:
                company = self.companies_collection.find_one({
                    "_id": material["company_id"]
                })
                
                if not company:
                    continue
                
                total_stock = self._get_total_stock(str(material["_id"]))
                
                results.append({
                    "id": str(material["_id"]),
                    "name": material["name"],
                    "price": material.get("price", 0),
                    "units": material.get("units", "unidad"),
                    "company_id": str(company["_id"]),
                    "company_name": company["name"],
                    "company_address": company.get("address", ""),
                    "available_stock": total_stock
                })
            
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al buscar productos: {str(e)}")

    def _get_total_stock(self, material_id: str):
        try:
            stocks = list(self.location_stock_collection.find({
                "type_material_id": ObjectId(material_id)
            }))
            total = sum(stock.get("stock", 0) for stock in stocks)
            return total
        except:
            return 0