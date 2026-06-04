from pydantic import BaseModel
from typing import List, Optional

class EstadoActuadoresDTO(BaseModel):
    Valvula: int
    Manual: int

class MetricasAguaDTO(BaseModel):
    Lmin: float
    Total_L: float

class MetricasAmbientalesDTO(BaseModel):
    Suelo_RAW: float
    Temp_C: float
    Hum_Pct: float
    pH: float
    CO2: float
    Lux: float

class SistemaDTO(BaseModel):
    Memoria_SD_Pct: float

class TelemetriaRecordDTO(BaseModel):
    TS: str
    Nodo_ID: str
    Descripcion: str
    Estado_Actuadores: EstadoActuadoresDTO
    Metricas_Agua: MetricasAguaDTO
    Metricas_Ambientales: MetricasAmbientalesDTO
    Sistema: SistemaDTO

class LocalBackupLogDTO(BaseModel):
    fileName: str
    data: List[TelemetriaRecordDTO]