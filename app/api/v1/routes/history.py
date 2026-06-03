from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.history import LocalBackupLog
from app.crud import crud_history

router = APIRouter()

@router.post("/upload")
def upload_telemetry(log: LocalBackupLog, db: Session = Depends(get_db)):
    records_count = crud_history.bulk_insert_telemetry(db, log=log)
    return {"status": "success", "records_uploaded": records_count}

@router.get("/stats/{nodo_id}")
def get_node_stats(nodo_id: str, db: Session = Depends(get_db)):
    stats = crud_history.get_metrics_by_node(db, nodo_id=nodo_id)
    return {
        "nodo": nodo_id,
        "temp_promedio": round(stats.avg_temp or 0, 2),
        "humedad_promedio": round(stats.avg_hum or 0, 2),
        "ph_promedio": round(stats.avg_ph or 0, 2),
        "consumo_total_agua": stats.total_water or 0
    }