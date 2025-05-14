from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(length=250), ForeignKey("users.email"))
    weight = Column(Float)
    height = Column(Float)
    physical_activity = Column(Integer) # Actividad fisica
    fat = Column(Float)                 # Grasa corporal
    muscle = Column(Float)              # Masa muscular
    chest = Column(Float)               # medida Pecho
    waist = Column(Float)               # medida Cintura
    hips = Column(Float)                # medida Caderas
    biceps = Column(Float)              # medida Bíceps
    thigh = Column(Float)               # medida Muslos
    notes = Column(String(length=255))  # Notas
    date = Column(Date)

    users = relationship("User", back_populates="profiles")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}