from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PlantCreate(BaseModel):
    greenhouse_id: int = Field(..., alias="greenhouseId")
    species_id: int = Field(..., alias="speciesId")
    zone: str
    stage: Optional[str] = "Germinación"
    count: int = 1

class PlantUpdate(BaseModel):
    stage: Optional[str] = None
    status: Optional[str] = None
    count: Optional[int] = None
    is_critical: Optional[bool] = None

class PlantOut(BaseModel):
    id: int
    zone: str
    stage: str
    count: int
    status: str
    is_critical: bool = Field(..., alias="isCritical")
    planted_at: datetime = Field(..., alias="plantedAt")

    class Config:
        from_attributes = True
        populate_by_name = True