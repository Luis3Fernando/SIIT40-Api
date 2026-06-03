from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.schemas.specie import SpecieOutDTO

class PlantCreateDTO(BaseModel):
    greenhouse_id: int
    species_id: UUID
    zone: str
    stage: str
    count: Optional[int] = 1

class PlantUpdateDTO(BaseModel):
    zone: Optional[str] = None
    stage: Optional[str] = None
    count: Optional[int] = None
    is_critical: Optional[bool] = None
    status: Optional[str] = None

class PlantOutDTO(BaseModel):
    id: int
    greenhouse_id: int
    species_id: UUID
    zone: str
    stage: str
    count: int
    is_critical: bool
    last_watered: Optional[datetime]
    status: str
    planted_at: datetime
    specie: Optional[SpecieOutDTO] = None

    class Config:
        from_attributes = True