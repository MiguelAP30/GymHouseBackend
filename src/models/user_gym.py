from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class UserGym(Base):
    __tablename__ = "users_gyms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(length=250), ForeignKey("users.email"))
    gym_id = Column(Integer, ForeignKey("gyms.id"))
    start_date = Column(Date)
    final_date = Column(Date)
    is_active = Column(Boolean)

    users = relationship("User", back_populates="users_gyms")
    gyms = relationship("Gym", back_populates="users_gyms")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}