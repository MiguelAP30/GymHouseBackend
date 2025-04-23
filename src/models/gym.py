from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class Gym(Base):
    __tablename__ = "gyms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(length=250), ForeignKey("users.email"))
    name = Column(String(length=100))
    address = Column(String(length=100))
    phone = Column(String(length=20))
    email = Column(String(length=250))
    website = Column(String(length=100))
    open_time = Column(String(length=10))
    close_time = Column(String(length=10))
    price = Column(Float)
    description = Column(String(length=200))
    image = Column(String(length=100))
    city = Column(String(length=60))
    country = Column(String(length=60))
    start_date = Column(Date)
    final_date = Column(Date)
    is_active = Column(Boolean)
    max_users = Column(Integer, default=15)
    current_users = Column(Integer, default=0)

    users = relationship("User", back_populates="gyms")
    users_gyms = relationship("UserGym", back_populates="gyms")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}