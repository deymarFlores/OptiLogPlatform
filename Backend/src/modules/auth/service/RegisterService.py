from src.core.database import db
from src.modules.auth.schemas.AuthSchema import RegisterSchema
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register(data: RegisterSchema):
    try:
        # Verificar si el usuario ya existe
        users_collection = db["users"]
        existing_user = users_collection.find_one({"email": data.email})
        
        if existing_user:
            raise HTTPException(status_code=400, detail="El usuario ya existe")
        
        # Hashear contraseña
        hashed_password = pwd_context.hash(data.password)
        
        # Crear nuevo usuario
        new_user = {
            "name": data.name,
            "role": data.role,
            "email": data.email,
            "password": hashed_password
        }
        
        result = users_collection.insert_one(new_user)
        
        return {
            "message": "Registro exitoso",
            "user_id": str(result.inserted_id),
            "email": data.email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el registro: {str(e)}")
