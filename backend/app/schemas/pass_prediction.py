from pydantic import BaseModel
from datetime import datetime
from typing import List


class PassPredictionBase(BaseModel):
    aos_time: datetime
    los_time: datetime
    max_elevation: float
    duration: int
    quality_score: float


class PassPredictionCreate(PassPredictionBase):
    user_id: int
    satellite_id: int


class PassPredictionResponse(PassPredictionBase):
    id: int
    satellite_id: int

    class Config:
        from_attributes = True


class PassPredictionRequest(BaseModel):
    """Request body for calculating pass predictions"""
    latitude: float
    longitude: float
    days_ahead: int = 7


class PassPredictionWithSatellite(PassPredictionResponse):
    """Pass prediction with satellite details"""
    satellite_name: str
    satellite_category: str
