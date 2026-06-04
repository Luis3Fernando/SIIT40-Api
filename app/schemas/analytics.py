from pydantic import BaseModel
from datetime import datetime

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