from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Verify Supabase JWT token and return the current user.
    Creates user in local database if they don't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token from Supabase
        payload = jwt.decode(
            credentials.credentials,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )

        supabase_user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if supabase_user_id is None or email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Check if user exists in local database
    user = db.query(User).filter(User.supabase_id == supabase_user_id).first()

    # Create user if they don't exist
    if user is None:
        user = User(
            supabase_id=supabase_user_id,
            email=email
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication - returns None if no valid token is provided.
    """
    if credentials is None:
        return None

    try:
        # Decode JWT token from Supabase
        payload = jwt.decode(
            credentials.credentials,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated"
        )

        supabase_user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if supabase_user_id is None or email is None:
            return None

    except JWTError:
        return None

    # Check if user exists in local database
    user = db.query(User).filter(User.supabase_id == supabase_user_id).first()

    # Create user if they don't exist
    if user is None:
        user = User(
            supabase_id=supabase_user_id,
            email=email
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
