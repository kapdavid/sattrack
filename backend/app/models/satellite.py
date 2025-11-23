from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Satellite(Base):
    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True, index=True)
    norad_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)  # weather, amateur_radio, popular
    tle_line1 = Column(String, nullable=False)
    tle_line2 = Column(String, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    favorites = relationship("Favorite", back_populates="satellite", cascade="all, delete-orphan")
    pass_predictions = relationship("PassPrediction", back_populates="satellite", cascade="all, delete-orphan")
    notification_preferences = relationship("NotificationPreference", back_populates="satellite", cascade="all, delete-orphan")
