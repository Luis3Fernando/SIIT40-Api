from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.base_response import APIResponse
from app.schemas.history import LocalBackupLogDTO
from app.services.history import history_service
from app.utils.response_helper import ResponseHelper

router = APIRouter()

@router.post("/upload", response_model=APIResponse)
def upload_telemetry(log: LocalBackupLogDTO, db: Session = Depends(get_db)):
    inserted_count = history_service.upload_telemetry_bulk(db, log)
    return ResponseHelper.success(
        message="Sincronización masiva completada con éxito",
        data={"recordsUploaded": inserted_count, "fileName": log.fileName}
    )