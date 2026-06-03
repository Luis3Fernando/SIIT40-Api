from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SpecieOutDTO(BaseModel):
    species_id: int
    name: str
    scientific_name: str
    image_url: Optional[str]
    color: Optional[str]
    vol: Optional[float]
    freq: Optional[int]
    raw: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True

class SpecieUpdateDTO(BaseModel):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    color: Optional[str] = None
    vol: Optional[float] = None
    freq: Optional[int] = None
    raw: Optional[float] = None