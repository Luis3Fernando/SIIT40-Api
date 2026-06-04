from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.history import TelemetryHistory

class StatisticsService:
    def get_greenhouse_summary(self, db: Session, greenhouse_id: int, nodo_id: str = None, date_filter: str = None):
        query = db.query(
            func.min(TelemetryHistory.temp_c).label("min_temp"),
            func.max(TelemetryHistory.temp_c).label("max_temp"),
            func.avg(TelemetryHistory.temp_c).label("avg_temp"),
            
            func.min(TelemetryHistory.hum_pct).label("min_hum"),
            func.max(TelemetryHistory.hum_pct).label("max_hum"),
            func.avg(TelemetryHistory.hum_pct).label("avg_hum"),
            
            func.min(TelemetryHistory.soil_raw).label("min_soil"),
            func.max(TelemetryHistory.soil_raw).label("max_soil"),
            func.avg(TelemetryHistory.soil_raw).label("avg_soil"),
            
            func.min(TelemetryHistory.ph).label("min_ph"),
            func.max(TelemetryHistory.ph).label("max_ph"),
            func.avg(TelemetryHistory.ph).label("avg_ph"),
            
            func.min(TelemetryHistory.co2).label("min_co2"),
            func.max(TelemetryHistory.co2).label("max_co2"),
            func.avg(TelemetryHistory.co2).label("avg_co2"),
            
            func.min(TelemetryHistory.lux).label("min_lux"),
            func.max(TelemetryHistory.lux).label("max_lux"),
            func.avg(TelemetryHistory.lux).label("avg_lux"),
            
            func.min(TelemetryHistory.flow_lmin).label("min_flow"),
            func.max(TelemetryHistory.flow_lmin).label("max_flow"),
            func.avg(TelemetryHistory.flow_lmin).label("avg_flow")
        ).filter(TelemetryHistory.greenhouse_id == greenhouse_id)

        if nodo_id:
            query = query.filter(TelemetryHistory.nodo_id == nodo_id)

        if date_filter:
            try:
                parsed_date = date.fromisoformat(date_filter)
                query = query.filter(func.date(TelemetryHistory.recorded_at) == parsed_date)
            except ValueError:
                pass 

        result = query.first()

        if not result or result.min_temp is None:
            return None

        return {
            "temperature": {"min": round(result.min_temp, 2), "max": round(result.max_temp, 2), "avg": round(result.avg_temp, 2)},
            "humidity": {"min": round(result.min_hum, 2), "max": round(result.max_hum, 2), "avg": round(result.avg_hum, 2)},
            "soil_raw": {"min": round(result.min_soil, 2), "max": round(result.max_soil, 2), "avg": round(result.avg_soil, 2)},
            "ph": {"min": round(result.min_ph, 2), "max": round(result.max_ph, 2), "avg": round(result.avg_ph, 2)},
            "co2": {"min": round(result.min_co2, 2), "max": round(result.max_co2, 2), "avg": round(result.avg_co2, 2)},
            "lux": {"min": round(result.min_lux, 2), "max": round(result.max_lux, 2), "avg": round(result.avg_lux, 2)},
            "water_flow": {"min": round(result.min_flow, 2), "max": round(result.max_flow, 2), "avg": round(result.avg_flow, 2)}
        }

statistics_service = StatisticsService()