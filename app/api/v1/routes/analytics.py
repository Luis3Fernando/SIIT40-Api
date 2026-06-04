from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.base_response import APIResponse
from app.schemas.analytics import TimeSeriesPointDTO
from app.services.analytics import analytics_service
from app.utils.response_helper import ResponseHelper

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/time-series/{gh_id}", response_model=APIResponse[List[TimeSeriesPointDTO]])
def get_greenhouse_time_series(
    gh_id: int,
    group_by: str = Query("hour"),
    nodo: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    series_data = analytics_service.get_historical_series(db, gh_id, group_by, nodo, start_date, end_date)
    return ResponseHelper.success(
        message="Series temporales completas obtenidas con éxito",
        data=series_data
    )