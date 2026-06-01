from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/api/logout")
async def logout():
    return {
        "success": True,
        "message": "Sesión cerrada exitosamente"
    }
