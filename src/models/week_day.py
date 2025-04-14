from sqlalchemy import Column, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class WeekDay(Base):
    __tablename__ = "week_days"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=20))

    workout_day_exercises = relationship("WorkoutDayExercise", back_populates="week_days")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}