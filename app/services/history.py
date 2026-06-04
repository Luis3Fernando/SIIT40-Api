from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.orm import Session
from app.models.history import TelemetryHistory
from app.schemas.history import LocalBackupLogDTO

class HistoryService:
    def upload_telemetry_bulk(self, db: Session, log: LocalBackupLogDTO) -> int:
        db.query(TelemetryHistory).filter(TelemetryHistory.file_name == log.fileName).delete()
        db.flush()

        bulk_records = []
        for entry in log.data:
            try:
                dt_parsed = datetime.strptime(entry.TS, "%Y/%m/%d %H:%M:%S")
            except ValueError:
                continue

            record_dict = {
                "greenhouse_id": 1,
                "nodo_id": entry.Nodo_ID,
                "file_name": log.fileName,
                "recorded_at": dt_parsed,
                "sd_status_pct": entry.Sistema.Memoria_SD_Pct,
                "soil_raw": int(entry.Metricas_Ambientales.Suelo_RAW),
                "temp_c": entry.Metricas_Ambientales.Temp_C,
                "hum_pct": entry.Metricas_Ambientales.Hum_Pct,
                "ph": entry.Metricas_Ambientales.pH,
                "co2": entry.Metricas_Ambientales.CO2,
                "lux": entry.Metricas_Ambientales.Lux,
                "flow_lmin": entry.Metricas_Agua.Lmin,
                "total_l": entry.Metricas_Agua.Total_L,
                "valve_open": bool(entry.Estado_Actuadores.Valvula),
                "is_manual": bool(entry.Estado_Actuadores.Manual)
            }
            bulk_records.append(record_dict)

        if bulk_records:
            db.execute(insert(TelemetryHistory), bulk_records)
            db.commit()

        return len(bulk_records)

history_service = HistoryService()