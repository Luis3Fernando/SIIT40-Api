from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.base_response import APIResponse
from app.schemas.auth import LoginDTO, TokenRefreshRequestDTO, LoginResponseDataDTO
from app.services.auth import auth_service
from app.utils.response_helper import ResponseHelper

router = APIRouter()

@router.post("/login", response_model=APIResponse[LoginResponseDataDTO])
def login(credentials: LoginDTO, db: Session = Depends(get_db)):
    result = auth_service.login(db, credentials)
    
    if "error" in result:
        return ResponseHelper.error(message=result["error"], msg_type="warning")
        
    return ResponseHelper.success(
        message="Autenticación exitosa. ¡Bienvenido!",
        data=result
    )

@router.post("/refresh", response_model=APIResponse)
def refresh_token(body: TokenRefreshRequestDTO):
    result = auth_service.refresh_token(body.refreshToken)
    
    if "error" in result:
        return ResponseHelper.error(message=f"No se pudo refrescar el token: {result['error']}")
        
    return ResponseHelper.success(
        message="Token actualizado correctamente",
        data=result
    )

@router.post("/logout", response_model=APIResponse)
def logout():
    return ResponseHelper.success(
        message="Sesión cerrada correctamente en el dispositivo"
    )