from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.like import Like
from src.models.training_plan import TrainingPlan
from src.models.user import User
from src.schemas.like import Like as LikeSchema

class LikeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_like(self, like: LikeSchema) -> Like:
        # Verificar si ya existe un like/dislike del usuario para este plan
        existing_like = self.db.query(Like).filter(
            Like.user_email == like.user_email,
            Like.training_plan_id == like.training_plan_id
        ).first()

        if existing_like:
            # Si existe, actualizar el estado del like
            existing_like.is_like = like.is_like
            self.db.commit()
            return existing_like

        # Si no existe, crear nuevo like/dislike
        db_like = Like(
            user_email=like.user_email,
            training_plan_id=like.training_plan_id,
            is_like=like.is_like
        )
        self.db.add(db_like)
        self.db.commit()
        self.db.refresh(db_like)
        return db_like

    def get_like_by_id(self, like_id: int) -> Like:
        return self.db.query(Like).filter(Like.id == like_id).first()

    def get_likes_by_training_plan(self, training_plan_id: int) -> list[Like]:
        return self.db.query(Like).filter(Like.training_plan_id == training_plan_id).all()

    def get_likes_by_user(self, user_email: str) -> list[Like]:
        return self.db.query(Like).filter(Like.user_email == user_email).all()

    def remove_like(self, like_id: int) -> bool:
        like = self.get_like_by_id(like_id)
        if like:
            self.db.delete(like)
            self.db.commit()
            return True
        return False

    def get_training_plan_likes_count(self, training_plan_id: int) -> int:
        return self.db.query(func.count(Like.id)).filter(
            Like.training_plan_id == training_plan_id,
            Like.is_like == True
        ).scalar()

    def get_training_plan_dislikes_count(self, training_plan_id: int) -> int:
        return self.db.query(func.count(Like.id)).filter(
            Like.training_plan_id == training_plan_id,
            Like.is_like == False
        ).scalar()

    def get_user_like_status(self, user_email: str, training_plan_id: int) -> Optional[bool]:
        like = self.db.query(Like).filter(
            Like.user_email == user_email,
            Like.training_plan_id == training_plan_id
        ).first()
        return like.is_like if like else None