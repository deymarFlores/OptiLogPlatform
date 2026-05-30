from pydantic import BaseModel, EmailStr

class TypeMaterialSchema(BaseModel):
    name: str
    price: float
    units: str