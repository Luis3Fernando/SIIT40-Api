from sqlalchemy import Column, Integer, BigInteger, String, Float, Boolean, DateTime, ForeignKey, func
from .base import Base

class TelemetryHistory(Base):
    __tablename__ = "telemetry_history"

    id = Column(BigInteger, primary_key=True, index=True)
    greenhouse_id = Column(Integer, ForeignKey("greenhouse.id"))
    nodo_id = Column(String)
    file_name = Column(String)
    recorded_at = Column(DateTime)
    sd_status_pct = Column(Float)
    
    soil_raw = Column(Integer)
    temp_c = Column(Float)
    hum_pct = Column(Float)
    ph = Column(Float)
    co2 = Column(Float)
    lux = Column(Float)
    
    flow_lmin = Column(Float)
    total_l = Column(Float)
    
    valve_open = Column(Boolean)
    is_manual = Column(Boolean)
    uploaded_at = Column(DateTime, server_default=func.now())