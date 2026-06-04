from fastapi import APIRouter
from app.api.v1.routes import auth
from app.api.v1.routes import utils
from app.api.v1.routes import specie
from app.api.v1.routes import plant
from app.api.v1.routes import history
from app.api.v1.routes import statistics
from app.api.v1.routes import analytics
from app.api.v1.routes import greenhouse

api_router = APIRouter()

api_router.include_router(utils.router, prefix="/utils", tags=["Utilidades / Pruebas"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(specie.router, prefix="/specie", tags=["Especies"])
api_router.include_router(plant.router, prefix="/plant", tags=["Plantas / Cultivos"])
api_router.include_router(history.router, prefix="/history", tags=["Historial de Telemetría"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["Módulo de Estadísticas"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Módulo de Analítica Avanzada"])
api_router.include_router(greenhouse.router, prefix="/greenhouse", tags=["Monitoreo de Invernadero"])