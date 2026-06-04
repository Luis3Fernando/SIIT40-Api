from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.base_response import APIResponse
from app.schemas.greenhouse import GreenhouseStatusOutDTO
from app.services.greenhouse import greenhouse_service
from app.utils.response_helper import ResponseHelper

router = APIRouter()

@router.get("/status/{gh_id}", response_model=APIResponse[GreenhouseStatusOutDTO])
def get_greenhouse_realtime_status(gh_id: int, db: Session = Depends(get_db)):
    status_data = greenhouse_service.get_current_status(db, gh_id)
    return ResponseHelper.success(
        message="Estado en tiempo real del invernadero obtenido",
        data=status_data
    )