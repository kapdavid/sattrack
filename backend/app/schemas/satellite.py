from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SatelliteBase(BaseModel):
    norad_id: int
    name: str
    category: str


class SatelliteCreate(SatelliteBase):
    tle_line1: str
    tle_line2: str


class SatelliteUpdate(BaseModel):
    tle_line1: Optional[str] = None
    tle_line2: Optional[str] = None


class SatelliteResponse(SatelliteBase):
    id: int
    tle_line1: str
    tle_line2: str
    last_updated: datetime

    class Config:
        from_attributes = True


class SatellitePosition(BaseModel):
    """Real-time satellite position"""
    latitude: float
    longitude: float
    altitude_km: float
    timestamp: datetime
