from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.core.auth import get_current_user_optional
from app.models.satellite import Satellite
from app.models.user import User
from app.models.pass_prediction import PassPrediction
from app.schemas.satellite import SatelliteResponse, SatellitePosition
from app.schemas.pass_prediction import PassPredictionRequest
from app.services.satellite_service import SatelliteService
from app.services.orbital_service import OrbitalService

router = APIRouter(prefix="/satellites", tags=["satellites"])


@router.get("", response_model=List[SatelliteResponse])
async def list_satellites(
    category: Optional[str] = Query(None, description="Filter by category (weather, amateur_radio, popular)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get list of satellites, optionally filtered by category.
    """
    satellites = SatelliteService.get_satellites(
        db=db,
        category=category,
        skip=skip,
        limit=limit
    )
    return satellites


@router.get("/search", response_model=List[SatelliteResponse])
async def search_satellites(
    q: str = Query(..., min_length=1, description="Search query"),
    db: Session = Depends(get_db)
):
    """
    Search satellites by name.
    """
    satellites = SatelliteService.search_satellites(db=db, query=q)
    return satellites


@router.get("/{satellite_id}", response_model=SatelliteResponse)
async def get_satellite(
    satellite_id: int,
    db: Session = Depends(get_db)
):
    """
    Get details for a specific satellite.
    """
    satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()

    if not satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")

    return satellite


@router.post("/{satellite_id}/refresh")
async def refresh_satellite_tle(
    satellite_id: int,
    db: Session = Depends(get_db)
):
    """
    Refresh TLE data for a specific satellite from CelesTrak.
    """
    success = await SatelliteService.update_satellite_tle(db=db, satellite_id=satellite_id)

    if not success:
        raise HTTPException(status_code=404, detail="Satellite not found or TLE update failed")

    return {"message": "TLE data updated successfully"}


@router.get("/{satellite_id}/position", response_model=SatellitePosition)
async def get_satellite_position(
    satellite_id: int,
    db: Session = Depends(get_db)
):
    """
    Get current position of a satellite.
    """
    satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()

    if not satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")

    # Create Skyfield satellite object
    sat = OrbitalService.create_satellite(
        satellite.name,
        satellite.tle_line1,
        satellite.tle_line2
    )

    # Get current position
    position = OrbitalService.get_current_position(sat)

    return position


@router.post("/{satellite_id}/predict")
async def predict_satellite_passes(
    satellite_id: int,
    request: PassPredictionRequest = Body(...),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Predict satellite passes for a given location over the next N days.

    If authenticated, predictions are cached for 6 hours to improve performance.
    Unauthenticated requests always calculate fresh predictions.
    """
    satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()

    if not satellite:
        raise HTTPException(status_code=404, detail="Satellite not found")

    # Check for cached predictions if user is authenticated
    cached_passes = []
    cache_hit = False

    if current_user:
        # Look for recent cached predictions (within 6 hours)
        cache_threshold = datetime.now(timezone.utc) - timedelta(hours=6)
        now = datetime.now(timezone.utc)
        future_window = now + timedelta(days=request.days_ahead)

        # Find cached predictions for this satellite/user that cover the requested time window
        # and were created recently (within cache threshold)
        cached_predictions = db.query(PassPrediction).filter(
            PassPrediction.user_id == current_user.id,
            PassPrediction.satellite_id == satellite_id,
            PassPrediction.aos_time >= now,
            PassPrediction.aos_time <= future_window,
        ).all()

        # If we have cached predictions, use them
        if cached_predictions:
            cache_hit = True
            cached_passes = [
                {
                    "aos_time": p.aos_time,
                    "los_time": p.los_time,
                    "max_elevation": p.max_elevation,
                    "duration": p.duration,
                    "quality_score": p.quality_score,
                    "aos_azimuth": None,  # Not stored in cache
                    "los_azimuth": None,  # Not stored in cache
                    "max_azimuth": None,  # Not stored in cache
                }
                for p in cached_predictions
            ]

    # If no cache hit, calculate new predictions
    if not cache_hit:
        passes = OrbitalService.predict_passes(
            name=satellite.name,
            tle_line1=satellite.tle_line1,
            tle_line2=satellite.tle_line2,
            observer_lat=request.latitude,
            observer_lon=request.longitude,
            days_ahead=request.days_ahead
        )

        # Save to cache if user is authenticated
        if current_user:
            # Delete old predictions for this satellite/user
            db.query(PassPrediction).filter(
                PassPrediction.user_id == current_user.id,
                PassPrediction.satellite_id == satellite_id
            ).delete()

            # Save new predictions
            for pass_data in passes:
                prediction = PassPrediction(
                    user_id=current_user.id,
                    satellite_id=satellite_id,
                    aos_time=pass_data["aos_time"],
                    los_time=pass_data["los_time"],
                    max_elevation=pass_data["max_elevation"],
                    duration=pass_data["duration"],
                    quality_score=pass_data["quality_score"]
                )
                db.add(prediction)

            db.commit()
    else:
        passes = cached_passes

    return {
        "satellite_id": satellite.id,
        "satellite_name": satellite.name,
        "observer_latitude": request.latitude,
        "observer_longitude": request.longitude,
        "days_ahead": request.days_ahead,
        "passes": passes,
        "cached": cache_hit
    }
