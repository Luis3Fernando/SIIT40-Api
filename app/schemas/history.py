from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ActuadoresDTO(BaseModel):
    Valvula: int
    Manual: int

class AguaDTO(BaseModel):
    Lmin: float
    Total_L: float

class AmbientalesDTO(BaseModel):
    Suelo_RAW: int
    Temp_C: float
    Hum_Pct: float
    pH: float
    CO2: float
    Lux: float

class SistemaDTO(BaseModel):
    Memoria_SD_Pct: float

class TelemetriaDTO(BaseModel):
    TS: str
    Nodo_ID: str
    Descripcion: str
    Estado_Actuadores: ActuadoresDTO
    Metricas_Agua: AguaDTO
    Metricas_Ambientales: AmbientalesDTO
    Sistema: SistemaDTO

class LocalBackupLog(BaseModel):
    fileName: str
    data: List[TelemetriaDTO]