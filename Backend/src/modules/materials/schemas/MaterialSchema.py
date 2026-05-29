from pydantic import BaseModel, EmailStr

class MaterialSchema(BaseModel):
    name: str
    stock: int