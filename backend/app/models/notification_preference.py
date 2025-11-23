from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base


class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    __table_args__ = (
        UniqueConstraint('user_id', 'satellite_id', name='unique_user_satellite_notification'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    satellite_id = Column(Integer, ForeignKey("satellites.id", ondelete="CASCADE"), nullable=False)
    min_elevation = Column(Float, nullable=False, default=10.0)  # Minimum elevation to trigger notification
    email_enabled = Column(Boolean, nullable=False, default=True)
    push_enabled = Column(Boolean, nullable=False, default=False)

    # Relationships
    user = relationship("User", back_populates="notification_preferences")
    satellite = relationship("Satellite", back_populates="notification_preferences")
