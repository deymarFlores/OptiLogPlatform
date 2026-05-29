from pydantic import BaseModel, EmailStr

class CompanieSchema(BaseModel):
    name: str
    address: str
    phone: str