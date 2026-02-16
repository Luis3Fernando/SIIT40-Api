from pydantic import BaseModel, Field, field_validator
from typing import Optional

class SpecieOut(BaseModel):
    species_id: int = Field(..., alias="speciesId")
    name: str
    scientific_name: str = Field(..., alias="scientificName")
    image_url: Optional[str] = Field(None, alias="imageUrl")
    color: str
    vol: float
    freq: int
    raw: float

    @field_validator("image_url", mode="before")
    @classmethod
    def assemble_image_url(cls, v):
        if v and v.startswith("/static"):
            return f"http://localhost:8000{v}"
        return v

    class Config:
        from_attributes = True
        populate_by_name = True