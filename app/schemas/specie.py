from pydantic import BaseModel, Field, field_validator
from typing import Optional

class SpecieBase(BaseModel):
    speciesId: int = Field(..., alias="species_id")
    name: str
    scientificName: str = Field(..., alias="scientific_name")
    imageUrl: Optional[str] = Field(None, alias="image_url")
    color: str
    vol: float
    freq: int
    raw: float

    @field_validator("imageUrl", mode="before")
    @classmethod
    def assemble_image_url(cls, v):
        if v and v.startswith("/static"):
            return f"http://localhost:8000{v}"
        return v

    class Config:
        from_attributes = True 
        populate_by_name = True 