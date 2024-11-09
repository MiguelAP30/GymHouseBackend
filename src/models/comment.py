from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(length=250), ForeignKey("users.email"))
    training_plan_id = Column(Integer, ForeignKey("training_plans.id"))
    content = Column(String(length=200))
    date = Column(Date)

    users = relationship("User", back_populates="comments")
    training_plans = relationship("TrainingPlan", back_populates="comments")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}