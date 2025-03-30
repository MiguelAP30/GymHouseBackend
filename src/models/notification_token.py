from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class NotificationToken(Base):
    __tablename__ = "notification_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_email = Column(String(length=250), ForeignKey("users.email"))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="notification_tokens") 