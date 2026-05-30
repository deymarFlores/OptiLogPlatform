from src.core.database import db
from src.modules.locationsCompany.schemas.LocationCompanySchema import LocationCompanySchema
from fastapi import HTTPException
from bson.objectid import ObjectId


class LocationCompanyService:
    def __init__(self):
        self.collection = db["location_companies"]

    def _get_default_type_location(self, company_id: str):
        type_locations_collection = db["type_locations"]
        first_type = type_locations_collection.find_one(
            {"company_id": ObjectId(company_id)}
        )
        if first_type:
            return str(first_type["_id"])
        return None

    def create(self, company_id: str, data: LocationCompanySchema):
        try:
            location = {
                "company_id": ObjectId(company_id),
                "name": data.name,
                "lat": data.lat,
                "lng": data.lng,
                "type_location_id": ObjectId(data.type_location_id) if data.type_location_id else None
            }
            result = self.collection.insert_one(location)
            return {
                "id": str(result.inserted_id),
                "company_id": company_id,
                "name": data.name,
                "lat": data.lat,
                "lng": data.lng,
                "type_location_id": data.type_location_id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear location: {str(e)}")

    def get_by_company(self, company_id: str):
        try:
            locations = list(self.collection.find({"company_id": ObjectId(company_id)}))
            default_type_id = self._get_default_type_location(company_id)
            
            result = []
            for loc in locations:
                type_location_id = loc.get("type_location_id")
                
                if not type_location_id and default_type_id:
                    type_location_id = ObjectId(default_type_id)
                    self.collection.update_one(
                        {"_id": loc["_id"]},
                        {"$set": {"type_location_id": type_location_id}}
                    )
                    type_location_id_str = default_type_id
                elif type_location_id:
                    type_location_id_str = str(type_location_id)
                else:
                    type_location_id_str = ""
                
                result.append({
                    "id": str(loc["_id"]),
                    "company_id": str(loc["company_id"]),
                    "name": loc["name"],
                    "lat": loc["lat"],
                    "lng": loc["lng"],
                    "type_location_id": type_location_id_str
                })
            
            return result
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
                "lng": location["lng"],
                "type_location_id": str(location["type_location_id"]) if location.get("type_location_id") else ""
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener location: {str(e)}")

    def update(self, location_id: str, data: LocationCompanySchema):
        try:
            update_data = {
                "name": data.name,
                "lat": data.lat,
                "lng": data.lng
            }
            
            if data.type_location_id:
                update_data["type_location_id"] = ObjectId(data.type_location_id)
            
            result = self.collection.update_one(
                {"_id": ObjectId(location_id)},
                {"$set": update_data}
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