from fastapi import APIRouter
from app.schemas.base_response import APIResponse
from app.utils.response_helper import ResponseHelper

router = APIRouter()

@router.get("/saludo", response_model=APIResponse)
def saludo_tesis(usuario: str = "Invitado"):

    payload = {
        "greenhouse": "SIIT40 Greenhouse API",
        "currentUser": usuario
    }
    
    return ResponseHelper.success(
        message=f"Hola {usuario}, consulta realizada con éxito", 
        data=payload
    )