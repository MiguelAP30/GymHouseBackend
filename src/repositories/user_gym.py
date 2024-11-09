from typing import List
from src.models.user_gym import UserGym as user_gym
from src.schemas.user_gym import UserGym

class UserGymRepository():
    def __init__(self, db) -> None:
        self.db = db

    def get_all_user_gym(self, current_user) -> List[UserGym]:
        query = self.db.query(user_gym).filter(user_gym.gym_id == current_user)
        return query.all()
    
    def create_new_user_gym(self, user_gym: UserGym) -> UserGym:
        new_user_gym = user_gym(**user_gym.model_dump())
        self.db.add(new_user_gym)

        self.db.commit()
        self.db.refresh(new_user_gym)
        return new_user_gym
    
    def delete_user_gym(self, id: int) -> dict:
        element = self.db.query(user_gym).filter(user_gym.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return {"message": "The user_gym was successfully deleted", "data": None}
    
    def update_user_gym(self, id: int, user_gym: UserGym) -> UserGym:
        element = self.db.query(user_gym).filter(user_gym.id == id).first()
        for var, value in user_gym.model_dump().items():
            setattr(element, var, value)
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def get_user_gym_by_id(self, id: int) -> UserGym:
        element = self.db.query(user_gym).filter(user_gym.id == id).first()
        return element
    
    def get_user_gym_by_user_id(self, user_id: int) -> UserGym:
        element = self.db.query(user_gym).filter(user_gym.user_id == user_id).first()
        return element