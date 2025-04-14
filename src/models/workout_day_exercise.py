from sqlalchemy import Column, ForeignKey, Integer, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class WorkoutDayExercise(Base):
    __tablename__ = "workout_day_exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    week_day_id = Column(Integer, ForeignKey("week_days.id"))
    training_plan_id = Column(Integer, ForeignKey("training_plans.id"))

    week_days = relationship("WeekDay", back_populates="workout_day_exercises")
    training_plans = relationship("TrainingPlan", back_populates="workout_day_exercises")
    exercise_configurations = relationship("ExerciseConfiguration", back_populates="workout_day_exercise")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}