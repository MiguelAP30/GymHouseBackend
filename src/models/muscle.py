from sqlalchemy import Column, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class Muscle(Base):
    __tablename__ = "muscles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))
    description = Column(String(length=200))

    specific_muscles = relationship("SpecificMuscle", back_populates="muscles")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}