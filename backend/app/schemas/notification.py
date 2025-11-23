from pydantic import BaseModel


class NotificationPreferenceBase(BaseModel):
    satellite_id: int
    min_elevation: float = 10.0
    email_enabled: bool = True
    push_enabled: bool = False


class NotificationPreferenceCreate(NotificationPreferenceBase):
    pass


class NotificationPreferenceUpdate(BaseModel):
    min_elevation: float | None = None
    email_enabled: bool | None = None
    push_enabled: bool | None = None


class NotificationPreferenceResponse(NotificationPreferenceBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
