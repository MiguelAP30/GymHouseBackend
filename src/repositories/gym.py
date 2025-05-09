from typing import List
from src.models.gym import Gym as GymModel  # Modelo SQLAlchemy
from src.schemas.gym import Gym as GymSchema  # Esquema Pydantic

class GymRepository:
    def __init__(self, db) -> None:
        self.db = db

    def get_all_gym(self) -> List[GymModel]:
        query = self.db.query(GymModel)
        return query.all()

    def create_new_gym(self, gym: GymSchema) -> GymModel:
        new_gym = GymModel(**gym.model_dump())
        self.db.add(new_gym)
        self.db.commit()
        self.db.refresh(new_gym)
        return new_gym

    def delete_gym(self, id: int) -> dict:
        element = self.db.query(GymModel).filter(GymModel.id == id).first()
        if element:
            self.db.delete(element)
            self.db.commit()
        return element

    def get_gym_by_id(self, id: int) -> GymModel:
        element = self.db.query(GymModel).filter(GymModel.id == id).first()
        return element

    def get_gym_by_user(self, user: str) -> GymModel:
        element = self.db.query(GymModel).filter(GymModel.user_email == user).first()
        return element

    def delete_gym_by_id(self, id: int) -> dict:
        element = self.db.query(GymModel).filter(GymModel.id == id).first()
        if element:
            self.db.delete(element)
            self.db.commit()
        return element

    def delete_gym_by_user(self, user_email: str) -> dict:
        element = self.db.query(GymModel).filter(GymModel.user_email == user_email).first()
        if element:
            self.db.delete(element)
            self.db.commit()
        return element

    def update_gym_by_id(self, id: int, gym: GymSchema) -> GymModel:
        element = self.db.query(GymModel).filter(GymModel.id == id).first()
        if element:
            for key, value in gym.model_dump().items():
                setattr(element, key, value)
            self.db.commit()
            self.db.refresh(element)
        return element

    def update_gym_by_user(self, user_email: str, gym: GymSchema) -> GymModel:
        element = self.db.query(GymModel).filter(GymModel.user_email == user_email).first()
        if element:
            gym_data = gym.model_dump()
            gym_data.pop('id', None)
            gym_data.pop('user_email', None)
            for key, value in gym_data.items(): 
                setattr(element, key, value)
            self.db.commit()
            self.db.refresh(element)
        return element
    
    def get_gym_by_email(self, email: str) -> GymModel:
        return self.db.query(GymModel).filter(GymModel.user_email == email).first()
    
    def increase_max_users (self, gym_id: int, new_max_users: int) -> dict:
        """
        Aumenta el límite máximo de usuarios de un gimnasio.
        
        Args:
            gym_id: ID del gimnasio
            new_max_users: Nuevo límite máximo de usuarios
            
        Returns:
            El gimnasio actualizado
        """
        if new_max_users <= 0:
            raise ValueError("El nuevo límite de usuarios debe ser mayor que 0")
        
        # Obtener el gimnasio
        gym = self.db.query(GymModel).filter(GymModel.id == gym_id).first()
        if not gym:
            raise ValueError("El gimnasio no existe")
        
        # Verificar que el nuevo límite no sea menor que el número actual de usuarios
        if new_max_users < gym.current_users:
            raise ValueError("El nuevo límite no puede ser menor que el número actual de usuarios")
        
        # Actualizar el límite máximo
        gym.max_users = new_max_users
        self.db.commit()
        self.db.refresh(gym)
        
        return {"message": "Límite de usuarios actualizado exitosamente", "data": gym}
