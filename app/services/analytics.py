from sqlalchemy.orm import Session
from app.models.history import TelemetryHistory
from sqlalchemy import func, cast, Integer

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

    def get_water_analytics(self, db: Session, greenhouse_id: int, bucket_unit: str = "month", start_date: str = None, end_date: str = None):
        unit = "month" if bucket_unit == "month" else "day"
        time_bucket = func.date_trunc(unit, TelemetryHistory.recorded_at).label("time_bucket")

        global_totals = db.query(
            func.sum(TelemetryHistory.total_l).label("total_l"),
            func.sum(cast(TelemetryHistory.valve_open, Integer)).label("total_events")
        ).filter(TelemetryHistory.greenhouse_id == greenhouse_id)

        if start_date:
            global_totals = global_totals.filter(TelemetryHistory.recorded_at >= start_date)
        if end_date:
            global_totals = global_totals.filter(TelemetryHistory.recorded_at <= end_date)

        global_res = global_totals.first()
        global_liters = round(global_res.total_l, 2) if global_res and global_res.total_l is not None else 0.0
        global_events = global_res.total_events if global_res and global_res.total_events is not None else 0

        breakdown_query = db.query(
            time_bucket,
            func.sum(TelemetryHistory.total_l).label("bucket_liters"),
            func.avg(TelemetryHistory.flow_lmin).label("bucket_flow"),
            func.sum(cast(TelemetryHistory.valve_open, Integer)).label("bucket_events")
        ).filter(TelemetryHistory.greenhouse_id == greenhouse_id)

        if start_date:
            breakdown_query = breakdown_query.filter(TelemetryHistory.recorded_at >= start_date)
        if end_date:
            breakdown_query = breakdown_query.filter(TelemetryHistory.recorded_at <= end_date)

        breakdown_results = breakdown_query.group_by("time_bucket").order_by("time_bucket").all()

        breakdown_list = [
          {
              "time_bucket": row.time_bucket,
              "total_liters": round(row.bucket_liters, 2) if row.bucket_liters is not None else 0.0,
              "average_flow_rate": round(row.bucket_flow, 2) if row.bucket_flow is not None else 0.0,
              "irrigation_events": row.bucket_events if row.bucket_events is not None else 0
          }
          for row in breakdown_results
        ]

        return {
            "greenhouse_id": greenhouse_id,
            "global_total_liters": global_liters,
            "global_irrigation_events": global_events,
            "breakdown": breakdown_list
        }
        
analytics_service = AnalyticsService()