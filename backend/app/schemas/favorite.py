from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.satellite import SatelliteResponse
from app.schemas.pass_prediction import PassPredictionResponse


class FavoriteBase(BaseModel):
    satellite_id: int


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    satellite_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteWithSatellite(FavoriteResponse):
    """Favorite with satellite details"""
    satellite: SatelliteResponse


class FavoriteWithPasses(FavoriteWithSatellite):
    """Favorite with satellite and upcoming passes"""
    upcoming_passes: List[PassPredictionResponse]
