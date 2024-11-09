from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class Dificulty(Base):
    __tablename__ = "dificulties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=20))

    exercises = relationship("Exercise", back_populates="dificulties")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}