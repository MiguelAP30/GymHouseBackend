from sqlalchemy import Column, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class TagOfTrainingPlan(Base):
    __tablename__ = "tags_of_training_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=50))

    training_plans = relationship("TrainingPlan", back_populates="tags_of_training_plans")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}