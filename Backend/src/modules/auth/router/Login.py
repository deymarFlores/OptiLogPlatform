from fastapi import APIRouter
from src.modules.auth.schemas.AuthSchema import LoginSchema
from src.modules.auth.service.LoginService import login as login_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(data: LoginSchema):
    return login_service(data)
