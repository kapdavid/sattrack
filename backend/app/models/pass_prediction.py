from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class PassPrediction(Base):
    __tablename__ = "pass_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    satellite_id = Column(Integer, ForeignKey("satellites.id", ondelete="CASCADE"), nullable=False, index=True)
    aos_time = Column(DateTime(timezone=True), nullable=False, index=True)  # Acquisition of Signal
    los_time = Column(DateTime(timezone=True), nullable=False)  # Loss of Signal
    max_elevation = Column(Float, nullable=False)  # degrees above horizon
    duration = Column(Integer, nullable=False)  # seconds
    quality_score = Column(Float, nullable=False, index=True)  # 0-100 score based on elevation and duration

    # Relationships
    user = relationship("User", back_populates="pass_predictions")
    satellite = relationship("Satellite", back_populates="pass_predictions")
