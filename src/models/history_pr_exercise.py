from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class HistoryPrExercise(Base):
    __tablename__ = "history_pr_exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(length=250), ForeignKey("users.email"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    date = Column(Date)
    notas = Column(String(length=500), nullable=True)
    tipo_sesion = Column(String(length=50), nullable=True)

    users = relationship("User", back_populates="history_pr_exercises")
    exercises = relationship("Exercise", back_populates="history_pr_exercises")
    series_pr_exercises = relationship("SeriesPrExercise", back_populates="history_pr_exercise", cascade="all, delete-orphan")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}