from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's profile.
    """
    return current_user


@router.put("/location", response_model=UserResponse)
async def update_user_location(
    location: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user's observer location (latitude/longitude).
    """
    if location.location_lat is not None:
        if not (-90 <= location.location_lat <= 90):
            raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90")
        current_user.location_lat = location.location_lat

    if location.location_lon is not None:
        if not (-180 <= location.location_lon <= 180):
            raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180")
        current_user.location_lon = location.location_lon

    db.commit()
    db.refresh(current_user)

    return current_user
