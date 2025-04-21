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
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    max_users = Column(Integer, default=15)  # Default number of users a gym can have
    current_users = Column(Integer, default=0)  # Current number of users associated

    users = relationship("User", back_populates="users_gyms")
    gyms = relationship("Gym", back_populates="users_gyms")
    training_plans = relationship("TrainingPlan", back_populates="user_gym")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}