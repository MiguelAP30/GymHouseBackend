from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, inspect
from sqlalchemy.orm import relationship
from src.config.database import Base

class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=60))
    description = Column(String(length=200))
    tag_of_training_plan_id = Column(Integer, ForeignKey("tags_of_training_plans.id"))
    user_email = Column(String(length=200), ForeignKey("users.email"))
    user_gym_id = Column(Integer, ForeignKey("users_gyms.id"), nullable=True)
    is_visible = Column(Boolean, default=False)
    is_gym_created = Column(Boolean, default=False)

    workout_day_exercises = relationship("WorkoutDayExercise", back_populates="training_plans")
    tags_of_training_plans = relationship("TagOfTrainingPlan", back_populates="training_plans")
    users = relationship("User", back_populates="training_plans")
    user_gym = relationship("UserGym", back_populates="training_plans")
    comments = relationship("Comment", back_populates="training_plans")
    likes = relationship("Like", back_populates="training_plans")

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}