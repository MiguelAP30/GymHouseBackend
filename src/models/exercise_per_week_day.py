from sqlalchemy import Column, ForeignKey, Integer, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class ExercisePerWeekDay(Base):
    __tablename__ = "exercises_per_week_days"

    id = Column(Integer, primary_key=True, autoincrement=True)
    week_day_id = Column(Integer, ForeignKey("week_days.id"))
    detail_exercise_id = Column(Integer, ForeignKey("details_exercises.id"))
    training_plan_id = Column(Integer, ForeignKey("training_plans.id"))

    week_days = relationship("WeekDay", back_populates="exercises_per_week_days")
    training_plans = relationship("TrainingPlan", back_populates="exercises_per_week_days")
    details_exercises = relationship("DetailedExercise", back_populates="exercises_per_week_days")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}