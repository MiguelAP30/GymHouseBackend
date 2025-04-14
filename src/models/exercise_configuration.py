from sqlalchemy import Column, ForeignKey, Integer, String, Float, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class ExerciseConfiguration(Base):
    __tablename__ = "exercise_configurations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    workout_day_exercise_id = Column(Integer, ForeignKey("workout_day_exercises.id"))
    sets = Column(Integer)
    reps = Column(Integer)
    rest = Column(Float)

    exercises = relationship("Exercise", back_populates="exercise_configurations")
    workout_day_exercise = relationship("WorkoutDayExercise", back_populates="exercise_configurations")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}