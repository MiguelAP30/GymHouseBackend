from sqlalchemy import Column, ForeignKey, Integer, String, Float, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class DetailedExercise(Base):
    __tablename__ = "details_exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exercice_muscle_id = Column(Integer, ForeignKey("exercises_muscles.id"))
    sets = Column(Integer)
    reps = Column(Integer)
    rest = Column(Float)

    exercises_muscles = relationship("ExerciseMuscle", back_populates="details_exercises")
    exercises_per_week_days = relationship("ExercisePerWeekDay", back_populates="details_exercises")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}