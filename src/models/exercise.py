from sqlalchemy import Column, ForeignKey, Integer, String, Date, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=60))
    description = Column(String(length=200))
    video = Column(String(length=200))
    image = Column(String(length=200))
    dateAdded = Column(Date)
    dificulty_id = Column(Integer, ForeignKey("dificulties.id"))
    machine_id = Column(Integer, ForeignKey("machines.id"))

    exercises_muscles = relationship("ExerciseMuscle", back_populates="exercises")
    history_pr_exercises = relationship("HistoryPrExercise", back_populates="exercises")
    dificulties = relationship("Dificulty", back_populates="exercises")
    machines = relationship("Machine", back_populates="exercises")
    exercise_configurations = relationship("ExerciseConfiguration", back_populates="exercises")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}