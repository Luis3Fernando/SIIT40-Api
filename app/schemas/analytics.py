from pydantic import BaseModel
from datetime import datetime
from typing import List
class TimeSeriesPointDTO(BaseModel):
    time_bucket: datetime
    nodo_id: str
    temp_c: float
    hum_pct: float
    soil_raw: float
    ph: float
    co2: float
    lux: float
    flow_lmin: float
    total_l: float

    class Config:
        from_attributes = True
        
class WaterBucketDTO(BaseModel):
    time_bucket: datetime
    total_liters: float
    average_flow_rate: float
    irrigation_events: int

    class Config:
        from_attributes = True

class WaterAnalyticsResponseDTO(BaseModel):
    greenhouse_id: int
    global_total_liters: float
    global_irrigation_events: int
    breakdown: List[WaterBucketDTO]

    class Config:
        from_attributes = True