from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.satellite import Satellite
from app.models.favorite import Favorite
from app.models.pass_prediction import PassPrediction
from app.schemas.favorite import FavoriteResponse, FavoriteCreate, FavoriteWithSatellite, FavoriteWithPasses
from app.schemas.pass_prediction import PassPredictionResponse

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("", response_model=List[FavoriteWithSatellite])
async def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all favorite satellites for the current user.
    """
    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    # Manually construct response with satellite details
    result = []
    for fav in favorites:
        satellite = db.query(Satellite).filter(Satellite.id == fav.satellite_id).first()
        result.append({
            "id": fav.id,
            "user_id": fav.user_id,
            "satellite_id": fav.satellite_id,
            "created_at": fav.created_at,
            "satellite": satellite
        })

    return result


@router.post("", response_model=FavoriteResponse)
async def add_favorite(
    favorite: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a satellite to favorites.
    """
    # Check if satellite exists
    satellite = db.query(Satellite).filter(Satellite.id == favorite.satellite_id).first()
    if not satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")

    # Check if already favorited
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.satellite_id == favorite.satellite_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Satellite already in favorites")

    # Create favorite
    new_favorite = Favorite(
        user_id=current_user.id,
        satellite_id=favorite.satellite_id
    )
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)

    return new_favorite


@router.delete("/{satellite_id}")
async def remove_favorite(
    satellite_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a satellite from favorites.
    """
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.satellite_id == satellite_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()

    return {"message": "Favorite removed successfully"}


@router.get("/passes", response_model=List[dict])
async def get_upcoming_passes_for_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get upcoming passes for all favorite satellites.
    Requires user to have a location set.
    """
    if current_user.location_lat is None or current_user.location_lon is None:
        raise HTTPException(
            status_code=400,
            detail="Please set your location first using PUT /api/user/location"
        )

    # Get all favorites
    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    if not favorites:
        return []

    # Get upcoming pass predictions for each favorite
    # For now, return recent predictions from database
    # In a production app, these would be pre-calculated by a background job
    now = datetime.utcnow()
    week_from_now = now + timedelta(days=7)

    passes = db.query(PassPrediction).filter(
        PassPrediction.user_id == current_user.id,
        PassPrediction.satellite_id.in_([f.satellite_id for f in favorites]),
        PassPrediction.aos_time >= now,
        PassPrediction.aos_time <= week_from_now
    ).order_by(PassPrediction.aos_time).all()

    # Format response with satellite details
    result = []
    for p in passes:
        satellite = db.query(Satellite).filter(Satellite.id == p.satellite_id).first()
        result.append({
            "id": p.id,
            "aos_time": p.aos_time,
            "los_time": p.los_time,
            "max_elevation": p.max_elevation,
            "duration": p.duration,
            "quality_score": p.quality_score,
            "satellite_id": p.satellite_id,
            "satellite_name": satellite.name if satellite else "Unknown",
            "satellite_category": satellite.category if satellite else "unknown"
        })

    return result
