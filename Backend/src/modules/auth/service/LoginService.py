from src.core.database import db
from src.modules.auth.schemas.AuthSchema import LoginSchema
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash
from fastapi import HTTPException

pwd_hasher = PasswordHasher()

def login(data: LoginSchema):
    try:
        users_collection = db["users"]
        user = users_collection.find_one({"email": data.email})
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        try:
            pwd_hasher.verify(user["password"], data.password)
        except (VerifyMismatchError, InvalidHash):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        return {
            "message": "Login exitoso",
            "user_id": str(user["_id"]),
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el login: {str(e)}")
