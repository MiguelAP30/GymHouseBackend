from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class SpecificMuscle(Base):
    __tablename__ = "specific_muscles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=40))
    muscle_id = Column(Integer, ForeignKey("muscles.id"))
    description = Column(String(length=200))

    muscles = relationship("Muscle", back_populates="specific_muscles")
    exercises_muscles = relationship("ExerciseMuscle", back_populates="specific_muscles")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}