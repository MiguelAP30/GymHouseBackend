from sqlalchemy import Column, ForeignKey, Integer, String, inspect, UniqueConstraint
from sqlalchemy.orm import relationship
from src.config.database import Base

class ExerciseMuscle(Base):
    __tablename__ = "exercises_muscles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    specific_muscle_id = Column(Integer, ForeignKey("specific_muscles.id"))
    rate = Column(Integer)

    exercises = relationship("Exercise", back_populates="exercises_muscles")
    specific_muscles = relationship("SpecificMuscle", back_populates="exercises_muscles")
    details_exercises = relationship("DetailedExercise", back_populates="exercises_muscles")

    __table_args__ = (UniqueConstraint('exercise_id', 'specific_muscle_id', name='uix_1'), )

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}