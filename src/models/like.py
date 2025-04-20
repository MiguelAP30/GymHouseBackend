from sqlalchemy import Column, ForeignKey, Integer, Float, Date, String, inspect, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(length=250), ForeignKey("users.email"))
    training_plan_id = Column(Integer, ForeignKey("training_plans.id"))
    is_like = Column(Boolean, default=True)  # True para like, False para dislike

    users = relationship("User", back_populates="likes")
    training_plans = relationship("TrainingPlan", back_populates="likes")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}