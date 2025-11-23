from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    supabase_id: str


class UserUpdate(BaseModel):
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None


class UserResponse(UserBase):
    id: int
    supabase_id: str
    location_lat: Optional[float]
    location_lon: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
