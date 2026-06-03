from fastapi import APIRouter
from app.api.v1.routes import auth
from app.api.v1.routes import utils
from app.api.v1.routes import specie

api_router = APIRouter()

api_router.include_router(utils.router, prefix="/utils", tags=["Utilidades / Pruebas"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(specie.router, prefix="/specie", tags=["Especies"])

# api_router.include_router(greenhouse.router, prefix="/greenhouse", tags=["Invernaderos"])
# api_router.include_router(plant.router, prefix="/plant", tags=["Plantas"])
# api_router.include_router(specie.router, prefix="/specie", tags=["Especies"])
# api_router.include_router(history.router, prefix="/history", tags=["Telemetría e Historial"])