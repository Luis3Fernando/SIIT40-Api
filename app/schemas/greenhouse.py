from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PlantSummaryDTO(BaseModel):
    total_plants_count: int
    active_crop_sectors: int
    has_critical_plants: bool

class LatestTelemetryDTO(BaseModel):
    recorded_at: datetime
    nodo_id: str
    temp_c: float
    hum_pct: float
    soil_raw: int
    ph: float
    co2: float
    lux: float
    valve_open: bool
    is_manual: bool
    sd_status_pct: float

class GreenhouseStatusOutDTO(BaseModel):
    greenhouse_id: int
    plant_summary: PlantSummaryDTO
    latest_telemetry: Optional[LatestTelemetryDTO] = None

    class Config:
        from_attributes = True