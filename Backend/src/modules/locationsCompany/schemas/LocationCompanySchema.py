from pydantic import BaseModel, EmailStr

class LocationCompanySchema(BaseModel):
    name: str
    lat: float
    lng: float