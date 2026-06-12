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
        window_sub = db.query(
            TelemetryHistory.greenhouse_id,
            TelemetryHistory.nodo_id,
            TelemetryHistory.recorded_at,
            TelemetryHistory.total_l,
            TelemetryHistory.flow_lmin,
            TelemetryHistory.valve_open,
            func.lag(TelemetryHistory.valve_open, 1, False).over(
                partition_by=[TelemetryHistory.greenhouse_id, TelemetryHistory.nodo_id],
                order_by=TelemetryHistory.recorded_at
            ).label("prev_valve")
        )

        if start_date:
            window_sub = window_sub.filter(TelemetryHistory.recorded_at >= start_date)
        if end_date:
            window_sub = window_sub.filter(TelemetryHistory.recorded_at <= end_date)

        w_sub = window_sub.subquery()

        daily_sub = db.query(
            func.date_trunc('day', w_sub.c.recorded_at).label("day_bucket"),
            w_sub.c.nodo_id,
            func.max(w_sub.c.total_l).label("daily_liters"),
            func.avg(w_sub.c.flow_lmin).label("daily_flow"),
            func.sum(cast((w_sub.c.valve_open == True) & (w_sub.c.prev_valve == False), Integer)).label("daily_events")
        ).filter(w_sub.c.greenhouse_id == greenhouse_id).group_by("day_bucket", w_sub.c.nodo_id).subquery()

        global_res = db.query(
            func.sum(daily_sub.c.daily_liters).label("total_l"),
            func.sum(daily_sub.c.daily_events).label("total_events")
        ).first()

        global_liters = round(global_res.total_l, 2) if global_res and global_res.total_l is not None else 0.0
        global_events = int(global_res.total_events) if global_res and global_res.total_events is not None else 0

        final_unit = "month" if bucket_unit == "month" else "day"
        time_bucket = func.date_trunc(final_unit, daily_sub.c.day_bucket).label("time_bucket")

        breakdown_results = db.query(
            time_bucket,
            func.sum(daily_sub.c.daily_liters).label("bucket_liters"),
            func.avg(daily_sub.c.daily_flow).label("bucket_flow"),
            func.sum(daily_sub.c.daily_events).label("bucket_events")
        ).group_by("time_bucket").order_by("time_bucket").all()

        breakdown_list = [
            {
                "time_bucket": row.time_bucket,
                "total_liters": round(row.bucket_liters, 2) if row.bucket_liters is not None else 0.0,
                "average_flow_rate": round(row.bucket_flow, 2) if row.bucket_flow is not None else 0.0,
                "irrigation_events": int(row.bucket_events) if row.bucket_events is not None else 0
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