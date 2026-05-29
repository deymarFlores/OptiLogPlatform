from src.core.database import db
from src.modules.locationsCompany.schemas.LocationCompanySchema import LocationCompanySchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class LocationCompanyService:
    def __init__(self):
        self.collection = db["location_companies"]

    def create(self, company_id: str, data: LocationCompanySchema):
        try:
            location = {
                "company_id": ObjectId(company_id),
                "name": data.name,
                "lat": data.lat,
                "lng": data.lng
            }
            result = self.collection.insert_one(location)
            return {
                "id": str(result.inserted_id),
                "company_id": company_id,
                "name": data.name,
                "lat": data.lat,
                "lng": data.lng
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear location: {str(e)}")

    def get_by_company(self, company_id: str):
        try:
            locations = list(self.collection.find({"company_id": ObjectId(company_id)}))
            return [
                {
                    "id": str(l["_id"]),
                    "name": l["name"],
                    "lat": l["lat"],
                    "lng": l["lng"]
                }
                for l in locations
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener locations: {str(e)}")

    def get_by_id(self, location_id: str):
        try:
            location = self.collection.find_one({"_id": ObjectId(location_id)})
            if not location:
                raise HTTPException(status_code=404, detail="Location no encontrada")
            return {
                "id": str(location["_id"]),
                "company_id": str(location["company_id"]),
                "name": location["name"],
                "lat": location["lat"],
                "lng": location["lng"]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener location: {str(e)}")

    def update(self, location_id: str, data: LocationCompanySchema):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(location_id)},
                {"$set": {
                    "name": data.name,
                    "lat": data.lat,
                    "lng": data.lng
                }}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Location no encontrada")
            return {"message": "Location actualizada"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar location: {str(e)}")

    def delete(self, location_id: str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(location_id)})
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Location no encontrada")
            return {"message": "Location eliminada"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar location: {str(e)}")
