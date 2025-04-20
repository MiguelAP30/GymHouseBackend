from sqlalchemy import Column, ForeignKey, Integer, Float, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class DropSetPrExercise(Base):
    __tablename__ = "dropset_pr_exercises"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    serie_pr_exercise_id = Column(Integer, ForeignKey("series_pr_exercises.id"))
    weight = Column(Float)
    reps = Column(Integer)
    orden_dropset = Column(Integer, nullable=True)

    serie_pr_exercise = relationship("SeriesPrExercise", back_populates="dropset_pr_exercises")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs} 