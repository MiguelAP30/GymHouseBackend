from fastapi import HTTPException, status 
from src.repositories.user import UserRepository 
from src.config.database import SessionLocal 
from src.auth import auth_handler 
from src.schemas.user import UserLogin as UserLoginSchema 
from src.schemas.user import User as UserCreateSchema
from src.services.email_service import EmailService
from src.models.user import User as UserModel
import random
import string
import traceback

class AuthRepository:
    def __init__(self) -> None:
        self.db = SessionLocal()
        self.email_service = EmailService()

    def generate_verification_code(self) -> str:
        verification_code = ''.join(random.choices(string.digits, k=6))
        return verification_code

    def register_user(self, user: UserCreateSchema) -> UserCreateSchema:
        try:
            # Verificar si el usuario ya existe
            existing_user = self.db.query(UserModel).filter(UserModel.email == user.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya existe"
                )

            # Generar código de verificación
            verification_code = self.generate_verification_code()

            # Hashear la contraseña antes de guardarla
            hashed_password = auth_handler.hash_password(user.password)

            # Crear nuevo usuario
            new_user = UserModel(
                email=user.email,
                id_number=user.id_number,
                password=hashed_password,  # Usar la contraseña hasheada
                user_name=user.user_name,
                name=user.name,
                phone=user.phone,
                address=user.address,
                birth_date=user.birth_date,
                gender=user.gender,
                is_verified=False,
                verification_code=verification_code
            )

            # Asignar rol por defecto (1 = usuario normal)
            new_user.role_id = 1

            # Guardar usuario en la base de datos
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            # Enviar correo de verificación
            email_sent = self.email_service.send_verification_email(user.email, verification_code)

            if not email_sent:
                print("ADVERTENCIA: No se pudo enviar el correo de verificación. El usuario deberá verificar su cuenta más tarde.")
                user.message = f"Usuario registrado exitosamente. Por favor verifica tu cuenta más tarde usando el código: {verification_code}"
            else:
                user.message = "Usuario registrado exitosamente. Por favor verifica tu email."

            return user

        except HTTPException as he:
            raise he
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def verify_email(self, email: str, verification_code: str) -> dict:
        db = SessionLocal()
        user = UserRepository(db).get_user_by_email(email=email)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
            
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya está verificado"
            )
            
        if user.verification_code != verification_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de verificación inválido"
            )
            
        user.is_verified = True
        user.verification_code = None
        db.commit()
        db.refresh(user)
        
        return {"message": "Email verificado exitosamente"}

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

    def resend_verification_code(self, email: str) -> dict:
        try:
            # Verificar si el usuario existe
            user = self.db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Verificar si el usuario ya está verificado
            if user.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario ya está verificado"
                )
            
            # Generar nuevo código de verificación
            new_verification_code = self.generate_verification_code()
            user.verification_code = new_verification_code
            
            # Guardar el nuevo código en la base de datos
            self.db.commit()
            self.db.refresh(user)
            
            # Enviar el nuevo código por correo
            email_sent = self.email_service.send_verification_email(email, new_verification_code)
            
            if not email_sent:
                return {
                    "message": "No se pudo enviar el correo de verificación. Tu nuevo código de verificación es: " + new_verification_code,
                    "verification_code": new_verification_code
                }
            
            return {
                "message": "Se ha enviado un nuevo código de verificación a tu correo electrónico",
                "verification_code": None
            }
            
        except HTTPException as he:
            raise he
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )