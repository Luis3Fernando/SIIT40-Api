from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.history import TelemetryHistory
from app.schemas.history import LocalBackupLog

def bulk_insert_telemetry(db: Session, log: LocalBackupLog) -> int:
    history_entries = []
    for entry in log.data:
        new_record = TelemetryHistory(
            greenhouse_id=1,  
            nodo_id=entry.Nodo_ID,
            file_name=log.fileName,
            recorded_at=datetime.fromisoformat(entry.TS.replace("Z", "+00:00")),
            sd_status_pct=entry.Sistema.Memoria_SD_Pct,
            soil_raw=entry.Metricas_Ambientales.Suelo_RAW,
            temp_c=entry.Metricas_Ambientales.Temp_C,
            hum_pct=entry.Metricas_Ambientales.Hum_Pct,
            ph=entry.Metricas_Ambientales.pH,
            co2=entry.Metricas_Ambientales.CO2,
            lux=entry.Metricas_Ambientales.Lux,
            flow_lmin=entry.Metricas_Agua.Lmin,
            total_l=entry.Metricas_Agua.Total_L,
            valve_open=bool(entry.Estado_Actuadores.Valvula),
            is_manual=bool(entry.Estado_Actuadores.Manual)
        )
        history_entries.append(new_record)
        
    db.add_all(history_entries)
    db.commit()
    return len(history_entries)

def get_metrics_by_node(db: Session, nodo_id: str):
    return db.query(
        func.avg(TelemetryHistory.temp_c).label("avg_temp"),
        func.avg(TelemetryHistory.hum_pct).label("avg_hum"),
        func.avg(TelemetryHistory.ph).label("avg_ph"),
        func.max(TelemetryHistory.total_l).label("total_water")
    ).filter(TelemetryHistory.nodo_id == nodo_id).first()