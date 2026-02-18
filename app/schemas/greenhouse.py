from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .plant import PlantOut

class GreenhouseCreate(BaseModel):
    name: str
    location: str
    latitude: float
    longitude: float
    userId: int = Field(..., alias="user_id")

class GreenhouseOut(BaseModel):
    id: int
    name: str
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime
    plants: List[PlantOut] = [] 
    plant_count: int = 0

    class Config:
        from_attributes = True
        populate_by_name = True