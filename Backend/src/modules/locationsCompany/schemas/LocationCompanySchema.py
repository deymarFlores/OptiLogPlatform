from pydantic import BaseModel

class LocationCompanySchema(BaseModel):
    name: str
    lat: float
    lng: float
    type_location_id: str