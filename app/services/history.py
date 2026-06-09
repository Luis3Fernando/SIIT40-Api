from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.models.history import TelemetryHistory
from app.schemas.history import LocalBackupLogDTO

class HistoryService:
    def upload_telemetry_bulk(self, db: Session, log: LocalBackupLogDTO) -> int:
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
            stmt = pg_insert(TelemetryHistory).values(bulk_records)
            stmt = stmt.on_conflict_do_update(
                constraint='_greenhouse_nodo_timestamp_uc',
                set_={
                    "file_name": stmt.excluded.file_name,
                    "sd_status_pct": stmt.excluded.sd_status_pct,
                    "soil_raw": stmt.excluded.soil_raw,
                    "temp_c": stmt.excluded.temp_c,
                    "hum_pct": stmt.excluded.hum_pct,
                    "ph": stmt.excluded.ph,
                    "co2": stmt.excluded.co2,
                    "lux": stmt.excluded.lux,
                    "flow_lmin": stmt.excluded.flow_lmin,
                    "total_l": stmt.excluded.total_l,
                    "valve_open": stmt.excluded.valve_open,
                    "is_manual": stmt.excluded.is_manual
                }
            )
            
            db.execute(stmt)
            db.commit()

        return len(bulk_records)

history_service = HistoryService()