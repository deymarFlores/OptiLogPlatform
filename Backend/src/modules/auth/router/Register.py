from fastapi import APIRouter
from src.modules.auth.schemas.AuthSchema import RegisterSchema
from src.modules.auth.service.RegisterService import register as register_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def register(data: RegisterSchema):
    return register_service(data)
