from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.history import TelemetryHistory

class AnalyticsService:
    def get_historical_series(self, db: Session, greenhouse_id: int, group_by: str, nodo_id: str = None, start_date: str = None, end_date: str = None):
        bucket_unit = "hour" if group_by == "hour" else "day"
        time_bucket = func.date_trunc(bucket_unit, TelemetryHistory.recorded_at).label("time_bucket")

        query = db.query(
            time_bucket,
            TelemetryHistory.nodo_id,
            func.avg(TelemetryHistory.temp_c).label("avg_temp"),
            func.avg(TelemetryHistory.hum_pct).label("avg_hum"),
            func.avg(TelemetryHistory.soil_raw).label("avg_soil"),
            func.avg(TelemetryHistory.ph).label("avg_ph"),
            func.avg(TelemetryHistory.co2).label("avg_co2"),
            func.avg(TelemetryHistory.lux).label("avg_lux"),
            func.avg(TelemetryHistory.flow_lmin).label("avg_flow"),
            func.avg(TelemetryHistory.total_l).label("avg_total")
        ).filter(TelemetryHistory.greenhouse_id == greenhouse_id)

        if nodo_id:
            query = query.filter(TelemetryHistory.nodo_id == nodo_id)

        if start_date:
            query = query.filter(TelemetryHistory.recorded_at >= start_date)
        if end_date:
            query = query.filter(TelemetryHistory.recorded_at <= end_date)

        results = query.group_by("time_bucket", TelemetryHistory.nodo_id).order_by("time_bucket").all()

        return [
            {
                "time_bucket": row.time_bucket,
                "nodo_id": row.nodo_id,
                "temp_c": round(row.avg_temp, 2) if row.avg_temp is not None else 0.0,
                "hum_pct": round(row.avg_hum, 2) if row.avg_hum is not None else 0.0,
                "soil_raw": round(row.avg_soil, 2) if row.avg_soil is not None else 0.0,
                "ph": round(row.avg_ph, 2) if row.avg_ph is not None else 0.0,
                "co2": round(row.avg_co2, 2) if row.avg_co2 is not None else 0.0,
                "lux": round(row.avg_lux, 2) if row.avg_lux is not None else 0.0,
                "flow_lmin": round(row.avg_flow, 2) if row.avg_flow is not None else 0.0,
                "total_l": round(row.avg_total, 2) if row.avg_total is not None else 0.0,
            }
            for row in results
        ]

analytics_service = AnalyticsService()