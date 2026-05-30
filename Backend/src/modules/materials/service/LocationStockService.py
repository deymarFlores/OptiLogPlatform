from src.core.database import db
from src.modules.materials.schemas.LocationStockSchema import LocationStockSchema, UpdateLocationStockSchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class LocationStockService:
    def __init__(self):
        self.collection = db["location_stocks"]
        self.materials_collection = db["type_materials"]

    def create(self, data: LocationStockSchema):
        try:
            # Verificar que el tipo de material existe
            material = self.materials_collection.find_one({"_id": ObjectId(data.type_material_id)})
            if not material:
                raise HTTPException(status_code=404, detail="Tipo de material no encontrado")

            # Verificar que no existe stock para esta combinación
            existing = self.collection.find_one({
                "location_id": ObjectId(data.location_id),
                "type_material_id": ObjectId(data.type_material_id)
            })
            if existing:
                raise HTTPException(status_code=400, detail="Este material ya existe en esta location")

            location_stock = {
                "location_id": ObjectId(data.location_id),
                "type_material_id": ObjectId(data.type_material_id),
                "stock": data.stock
            }
            result = self.collection.insert_one(location_stock)
            return {
                "id": str(result.inserted_id),
                "location_id": data.location_id,
                "type_material_id": data.type_material_id,
                "stock": data.stock
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear stock: {str(e)}")

    def get_by_location(self, location_id: str):
        try:
            stocks = list(self.collection.find({"location_id": ObjectId(location_id)}))
            result = []
            for stock in stocks:
                material = self.materials_collection.find_one({"_id": stock["type_material_id"]})
                result.append({
                    "id": str(stock["_id"]),
                    "location_id": str(stock["location_id"]),
                    "type_material_id": str(stock["type_material_id"]),
                    "material_name": material["name"],
                    "stock": stock["stock"],
                    "units": material["units"],
                    "price": material["price"]
                })
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener stocks: {str(e)}")

    def get_by_id(self, stock_id: str):
        try:
            stock = self.collection.find_one({"_id": ObjectId(stock_id)})
            if not stock:
                raise HTTPException(status_code=404, detail="Stock no encontrado")
            
            material = self.materials_collection.find_one({"_id": stock["type_material_id"]})
            return {
                "id": str(stock["_id"]),
                "location_id": str(stock["location_id"]),
                "type_material_id": str(stock["type_material_id"]),
                "material_name": material["name"],
                "stock": stock["stock"],
                "units": material["units"],
                "price": material["price"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener stock: {str(e)}")

    def update_stock(self, stock_id: str, data: UpdateLocationStockSchema):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(stock_id)},
                {"$set": {"stock": data.stock}}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Stock no encontrado")
            return {"message": "Stock actualizado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar stock: {str(e)}")

    def add_stock(self, stock_id: str, quantity: int):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(stock_id)},
                {"$inc": {"stock": quantity}}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Stock no encontrado")
            return {"message": f"Se agregaron {quantity} unidades"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al agregar stock: {str(e)}")

    def subtract_stock(self, stock_id: str, quantity: int):
        try:
            stock = self.collection.find_one({"_id": ObjectId(stock_id)})
            if not stock:
                raise HTTPException(status_code=404, detail="Stock no encontrado")
            
            if stock["stock"] < quantity:
                raise HTTPException(status_code=400, detail="Stock insuficiente")
            
            result = self.collection.update_one(
                {"_id": ObjectId(stock_id)},
                {"$inc": {"stock": -quantity}}
            )
            return {"message": f"Se restaron {quantity} unidades"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al restar stock: {str(e)}")

    def delete(self, stock_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(stock_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Stock no encontrado")
            return {"message": "Stock eliminado"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar stock: {str(e)}")
