from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.base_response import APIResponse
from app.schemas.statistics import GreenhouseStatsOutDTO
from app.services.statistics import statistics_service
from app.utils.response_helper import ResponseHelper

router = APIRouter()

@router.get("/greenhouse/{gh_id}", response_model=APIResponse[Optional[GreenhouseStatsOutDTO]])
def get_greenhouse_statistics(
    gh_id: int, 
    nodo: Optional[str] = Query(None, description="Filtrar por sub-nodo específico (A o B)"), 
    fecha: Optional[str] = Query(None, description="Filtrar por fecha específica (Formato: YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    stats = statistics_service.get_greenhouse_summary(db, gh_id, nodo, fecha)
    
    if not stats:
        return ResponseHelper.success(
            message="No hay datos de telemetría registrados para los filtros seleccionados",
            data=None
        )
        
    return ResponseHelper.success(
        message="Estadísticas procesadas correctamente",
        data=stats
    )