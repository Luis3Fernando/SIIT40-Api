from pydantic import BaseModel

class MetricStatsDTO(BaseModel):
    min: float
    max: float
    avg: float

class GreenhouseStatsOutDTO(BaseModel):
    temperature: MetricStatsDTO
    humidity: MetricStatsDTO
    soil_raw: MetricStatsDTO
    ph: MetricStatsDTO
    co2: MetricStatsDTO
    lux: MetricStatsDTO
    water_flow: MetricStatsDTO

    class Config:
        from_attributes = True