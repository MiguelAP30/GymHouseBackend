from fastapi import HTTPException, status 
from src.repositories.user import UserRepository 
from src.config.database import SessionLocal 
from src.auth import auth_handler 
from src.schemas.user import UserLogin as UserLoginSchema 
from src.schemas.user import User as UserCreateSchema

class AuthRepository:
    def __init__(self) -> None:
        pass

    def register_user(self, user: UserCreateSchema) -> dict:
        db = SessionLocal()
        user_repo = UserRepository(db)

        # Verificar si hay usuarios existentes
        existing_users = user_repo.get_all_users()
        
        # Asignar rol de administrador al primer usuario registrado
        if len(existing_users) == 0:
            role_id = 4  # Rol de administrador
        else:
            role_id = 1  # Rol por defecto (cambia esto según tu configuración)

        if UserRepository(db).get_user_by_email(email=user.email) is not None:
            raise Exception("La cuenta ya existe")
        hashed_password = auth_handler.hash_password(password=user.password)
        new_user: UserCreateSchema = UserCreateSchema(
            email=user.email,
            id_number=user.id_number,
            password=hashed_password,
            user_name=user.user_name,
            name=user.name,
            phone=user.phone,
            address=user.address,
            birth_date=user.birth_date,
            gender=user.gender,
            role_id=role_id
        )
        return UserRepository(db).create_new_user(new_user)

    def login_user(self, user: UserLoginSchema) -> dict:
        db = SessionLocal()
        check_user = UserRepository(db).get_user_by_email(email=user.email)
        if check_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas (1)",
            )
        if not auth_handler.verify_password(user.password, check_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas (2)",
            )
        if not check_user.status:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cuenta deshabilitada",
            )
        access_token = auth_handler.encode_token(check_user)
        refresh_token = auth_handler.encode_refresh_token(check_user)
        return access_token, refresh_token

    def change_password(self, email: str, current_password: str, new_password: str) -> dict:
        db = SessionLocal()
        user = UserRepository(db).get_user_by_email(email=email)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
            
        if not auth_handler.verify_password(current_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta",
            )
            
        hashed_password = auth_handler.hash_password(password=new_password)
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        return {"message": "Contraseña actualizada exitosamente"}

    def reset_password(self, email: str, new_password: str, reset_token: str) -> dict:
        db = SessionLocal()
        user = UserRepository(db).get_user_by_email(email=email)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
            
        # Verificar el token de restablecimiento
        if not auth_handler.verify_reset_token(reset_token, email):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de restablecimiento inválido o expirado",
            )
            
        hashed_password = auth_handler.hash_password(password=new_password)
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        return {"message": "Contraseña restablecida exitosamente"}

    def generate_reset_token(self, email: str) -> dict:
        db = SessionLocal()
        user = UserRepository(db).get_user_by_email(email=email)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )
            
        reset_token = auth_handler.encode_reset_token(user)
        return {"reset_token": reset_token}