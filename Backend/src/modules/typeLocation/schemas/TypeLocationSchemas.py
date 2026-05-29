from pydantic import BaseModel, EmailStr

class TypeLocationSchema(BaseModel):
    name: str
    icon: str
    color: str