from sqlalchemy import Column, ForeignKey, Integer, Float, inspect, String
from sqlalchemy.orm import relationship
from src.config.database import Base

class SeriesPrExercise(Base):
    __tablename__ = "series_pr_exercises"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    history_pr_exercise_id = Column(Integer, ForeignKey("history_pr_exercises.id"))
    weight = Column(Float)
    reps = Column(Integer)
    tipo_serie = Column(String(length=50), nullable=True)
    rpe = Column(Float, nullable=True)
    orden_serie = Column(Integer, nullable=True)
    notas_serie = Column(String(length=500), nullable=True)

    history_pr_exercise = relationship("HistoryPrExercise", back_populates="series_pr_exercises")
    dropset_pr_exercises = relationship("DropSetPrExercise", back_populates="serie_pr_exercise", cascade="all, delete-orphan")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs} 