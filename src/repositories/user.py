from typing import List, Optional
from sqlalchemy.orm import load_only
from src.schemas.user import User
from src.models.user import User as users
from datetime import date

class UserRepository():
    def __init__(self, db) -> None:
        self.db = db
    
    def get_all_users(self) -> List[User]:
        """
        Obtiene todos los usuarios y verifica sus fechas finales.
        Actualiza los roles de los usuarios cuya fecha ha pasado o no está definida.
        Solo se aplica a usuarios que no son administradores (rol 4).
        """
        elements = self.db.query(users).all()
        for element in elements:
            if element.role_id != 4 and (element.final_date is None or element.final_date < date.today()):
                element.role_id = 1  # Cambiar el rol a 1 (rol básico)
        self.db.commit()
        return [User(
            email=element.email,
            id_number=element.id_number,
            password=element.password,
            user_name=element.user_name,
            name=element.name,
            phone=element.phone,
            address=element.address,
            birth_date=element.birth_date,
            gender=element.gender,
            status=element.status,
            start_date=element.start_date,
            final_date=element.final_date,
            role_id=element.role_id,
            is_verified=element.is_verified,
            verification_code=element.verification_code
        ) for element in elements]
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email y verifica su fecha final.
        Si la fecha ha pasado o no está definida, actualiza su rol y estado.
        """
        element = self.db.query(users).filter(users.email == email).first()
        if element:
            if element.role_id != 4 and (element.final_date is None or element.final_date < date.today()):
                element.role_id = 1
                self.db.commit()
                self.db.refresh(element)
            return User(
                email=element.email,
                id_number=element.id_number,
                password=element.password,
                user_name=element.user_name,
                name=element.name,
                phone=element.phone,
                address=element.address,
                birth_date=element.birth_date,
                gender=element.gender,
                status=element.status,
                start_date=element.start_date,
                final_date=element.final_date,
                role_id=element.role_id,
                is_verified=element.is_verified,
                verification_code=element.verification_code
            )
        return None
    
    def delete_user(self, email: str ) -> dict:
        element: User= self.db.query(users).filter(users.email == email).first()
        element.status = False
        self.db.commit()
        self.db.refresh(element)
        return element

    def create_new_user(self, user:User ) -> dict:
        # Crear un diccionario con los datos del usuario, excluyendo el campo 'message'
        user_data = user.model_dump()
        if 'message' in user_data:
            del user_data['message']
            
        new_user = users(**user_data)
        self.db.add(new_user)
        
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update_user(self, email: str, user: User) -> dict:
        element = self.db.query(users).filter(users.email == email).first()
        element.id_number = user.id_number
        element.user_name = user.user_name
        element.name = user.name
        element.address = user.address
        element.phone = user.phone
        element.gender = user.gender
        element.birth_date = user.birth_date

        self.db.commit()
        self.db.refresh(element)
        return element

    def update_role(self, email: str, role_id: int, final_date: date) -> dict:
        """
        Actualiza el rol de un usuario y establece las fechas de inicio y finalización.
        
        Args:
            email: Email del usuario a actualizar
            role_id: Nuevo rol del usuario
            final_date: Fecha de finalización del rol
            
        Returns:
            Usuario actualizado
        """
        element = self.db.query(users).filter(users.email == email).first()
        if element:
            element.role_id = role_id
            element.start_date = date.today()  # Fecha actual como fecha de inicio
            element.final_date = final_date  # Fecha de finalización proporcionada
            self.db.commit()
            self.db.refresh(element)
        return element

    def update_verification_status(self, email: str, is_verified: bool) -> dict:
        """
        Actualiza el estado de verificación de un usuario.
        
        Args:
            email: Email del usuario a actualizar
            is_verified: Nuevo estado de verificación
            
        Returns:
            Usuario actualizado
        """
        element = self.db.query(users).filter(users.email == email).first()
        element.is_verified = is_verified
        self.db.commit()
        self.db.refresh(element)
        return element

    def get_user_model_by_email(self, email: str):
        """
        Obtiene el modelo SQLAlchemy de un usuario por su email.
        """
        return self.db.query(users).filter(users.email == email).first()
