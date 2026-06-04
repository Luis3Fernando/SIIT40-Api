from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.greenhouse import Plant
from app.models.history import TelemetryHistory

class GreenhouseService:
    def get_current_status(self, db: Session, greenhouse_id: int):
        total_plants = db.query(func.sum(Plant.count)).filter(
            Plant.greenhouse_id == greenhouse_id,
            Plant.status == "active"
        ).scalar() or 0

        active_sectors = db.query(func.count(Plant.id)).filter(
            Plant.greenhouse_id == greenhouse_id,
            Plant.status == "active"
        ).scalar() or 0

        has_critical = db.query(Plant.id).filter(
            Plant.greenhouse_id == greenhouse_id,
            Plant.status == "active",
            Plant.is_critical == True
        ).first() is not None

        latest_record = db.query(TelemetryHistory).filter(
            TelemetryHistory.greenhouse_id == greenhouse_id
        ).order_by(TelemetryHistory.recorded_at.desc()).first()

        telemetry_data = None
        if latest_record:
            telemetry_data = {
                "recorded_at": latest_record.recorded_at,
                "nodo_id": latest_record.nodo_id,
                "temp_c": latest_record.temp_c,
                "hum_pct": latest_record.hum_pct,
                "soil_raw": latest_record.soil_raw,
                "ph": latest_record.ph,
                "co2": latest_record.co2,
                "lux": latest_record.lux,
                "valve_open": latest_record.valve_open,
                "is_manual": latest_record.is_manual,
                "sd_status_pct": latest_record.sd_status_pct
            }

        return {
            "greenhouse_id": greenhouse_id,
            "plant_summary": {
                "total_plants_count": total_plants,
                "active_crop_sectors": active_sectors,
                "has_critical_plants": has_critical
            },
            "latest_telemetry": telemetry_data
        }

greenhouse_service = GreenhouseService()