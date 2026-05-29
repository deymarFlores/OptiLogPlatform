from src.core.database import db
from src.modules.auth.schemas.AuthSchema import LoginSchema
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def login(data: LoginSchema):
    try:
        users_collection = db["users"]
        
        # Buscar usuario por email
        user = users_collection.find_one({"email": data.email})
        
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        # Verificar contraseña
        if not pwd_context.verify(data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        return {
            "message": "Login exitoso",
            "user_id": str(user["_id"]),
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el login: {str(e)}")
