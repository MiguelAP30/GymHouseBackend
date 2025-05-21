from typing import List, Optional, Tuple
from sqlalchemy import and_, or_
from src.models.user_gym import UserGym as user_gym
from src.schemas.user_gym import UserGym, UserGymCreate, UserGymUpdateFinalDate
from src.models.user import User
from src.models.gym import Gym
from src.models.training_plan import TrainingPlan
from datetime import date

class UserGymRepository():
    def __init__(self, db) -> None:
        self.db = db

    def get_all_user_gym(self, current_user) -> List[user_gym]:
        query = self.db.query(user_gym).join(Gym, user_gym.gym_id == Gym.id).filter(Gym.user_email == current_user)
        return query.all()
    
    def create_new_user_gym(self, user_gym_data: UserGymCreate) -> UserGym:
        # Verificar que el gimnasio existe y obtener su información
        gym = self.db.query(Gym).filter(Gym.id == user_gym_data.gym_id).first()
        if not gym:
            raise ValueError("El gimnasio no existe")
        
        # Verificar que el usuario existe
        user = self.db.query(User).filter(User.email == user_gym_data.user_email).first()
        if not user:
            raise ValueError("El usuario no existe")
        
        # Verificar que el usuario no es un gimnasio
        if user.role_id == 3:
            raise ValueError("No se puede asociar un usuario gimnasio a otro gimnasio")
        
        # Verificar que el gimnasio no ha alcanzado su límite de usuarios
        if gym.current_users >= gym.max_users:
            raise ValueError("El gimnasio ha alcanzado su límite de usuarios")
        
        # Crear la nueva relación
        new_user_gym = user_gym(**user_gym_data.model_dump())
        new_user_gym.is_premium = True  # El usuario se convierte en premium
        
        # Actualizar el rol del usuario a premium (role_id = 2)
        user.role_id = 2
        user.start_date = user_gym_data.start_date
        user.final_date = user_gym_data.final_date
        
        # Incrementar el contador de usuarios del gimnasio
        gym.current_users += 1
        
        self.db.add(new_user_gym)
        self.db.commit()
        self.db.refresh(new_user_gym)
        return new_user_gym
    
    def remove_user_from_gym(self, gym_id: int, user_email: str) -> dict:
        """
        Elimina un usuario de un gimnasio y recupera su espacio.
        
        Args:
            gym_id: ID del gimnasio
            user_email: Email del usuario a eliminar
            
        Returns:
            El usuario eliminado
        """
        # Obtener la relación usuario-gimnasio
        user_gym_rel = self.db.query(user_gym).filter(
            and_(
                user_gym.gym_id == gym_id,
                user_gym.user_email == user_email
            )
        ).first()
        
        if not user_gym_rel:
            raise ValueError("El usuario no está asociado a este gimnasio")
        
        # Obtener el usuario y el gimnasio
        user = self.db.query(User).filter(User.email == user_email).first()
        gym = self.db.query(Gym).filter(Gym.id == gym_id).first()
        
        if not gym:
            raise ValueError("El gimnasio no existe")
        
        # Restaurar el rol del usuario a básico (role_id = 1)
        if user:
            user.role_id = 1
            user.final_date = None
        
        # Decrementar el contador de usuarios del gimnasio
        gym.current_users -= 1
        
        # Eliminar la relación
        self.db.delete(user_gym_rel)
        self.db.commit()
        
        return {"message": "Usuario eliminado exitosamente del gimnasio", "data": None}
    
    def update_user_gym(self, id: int, data: UserGymUpdateFinalDate) -> Optional[UserGym]:
        element = self.db.query(user_gym).filter(user_gym.id == id).first()
        if element:
            element.final_date = data.final_date

            # Actualizar el usuario si es necesario
            user = self.db.query(User).filter(User.email == element.user_email).first()
            if user:
                user.final_date = data.final_date

            self.db.commit()
            self.db.refresh(element)
            return element
        return None
    
    def get_user_gym_by_id(self, id: int) -> UserGym:
        element = self.db.query(user_gym).filter(user_gym.id == id).first()
        return element
    
    def get_user_gym_by_user_id(self, user_id: int) -> UserGym:
        element = self.db.query(user_gym).filter(user_gym.user_id == user_id).first()
        return element
    
    def get_gym_users(self, gym_id: int) -> List[UserGym]:
        """Obtiene todos los usuarios asociados a un gimnasio"""
        return self.db.query(user_gym).filter(user_gym.gym_id == gym_id).all()
    
    def get_user_gym(self, user_email: str, gym_id: int) -> Optional[UserGym]:
        """Obtiene la relación entre un usuario y un gimnasio"""
        return self.db.query(user_gym).filter(
            and_(
                user_gym.user_email == user_email,
                user_gym.gym_id == gym_id
            )
        ).first()
    
    def can_gym_manage_user_training_plan(self, gym_id: int, user_email: str) -> bool:
        """Verifica si un gimnasio puede gestionar los planes de entrenamiento de un usuario"""
        return self.db.query(user_gym).filter(
            and_(
                user_gym.gym_id == gym_id,
                user_gym.user_email == user_email,
                user_gym.is_active == True
            )
        ).first() is not None