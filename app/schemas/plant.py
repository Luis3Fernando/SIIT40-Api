from .specie import SpecieBase
from typing import Optional
from datetime import datetime
from pydantic import Field

class PlantOut(SpecieBase):
    id: int
    zone: str
    stage: str
    count: int
    isCritical: bool = Field(False, alias="is_critical")
    lastWatered: Optional[datetime] = Field(None, alias="last_watered")

    class Config:
        from_attributes = True
        populate_by_name = True