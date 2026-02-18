from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    full_name: Optional[str] = Field(None, alias="fullName")
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: Optional[str] = Field(None, alias="fullName")
    email: EmailStr
    created_at: datetime = Field(..., alias="createdAt")

    class Config:
        from_attributes = True
        populate_by_name = True