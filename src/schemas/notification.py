from pydantic import BaseModel
from typing import Optional

class NotificationTokenBase(BaseModel):
    token: str
    is_active: bool = True

class NotificationTokenCreate(NotificationTokenBase):
    pass

class NotificationToken(NotificationTokenBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Notification(BaseModel):
    title: str
    message: str
    token: str 