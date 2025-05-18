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

            # Verificar si hay algún usuario en la base de datos
            first_user = self.db.query(UserModel).first()
            
            # Asignar rol basado en si es el primer usuario
            role_id = 4 if first_user is None else 1

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
                verification_code=verification_code,
                role_id=role_id  # Asignar el rol correspondiente
            )

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
        try:
            # Verificar si el usuario existe
            user = self.db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
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
            
            # Marcar al usuario como verificado
            user.is_verified = True
            user.verification_code = None
            self.db.commit()
            
            return {"message": "Email verificado exitosamente"}
            
        except HTTPException as he:
            raise he
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def login_user(self, user: UserLoginSchema) -> dict:
        try:
            # Buscar el usuario directamente en la base de datos
            check_user = self.db.query(UserModel).filter(UserModel.email == user.email).first()
            
            if check_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                )
                
            if not auth_handler.verify_password(user.password, check_user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                )
            # Generar los tokens
            access_token = auth_handler.encode_token(check_user)
            refresh_token = auth_handler.encode_refresh_token(check_user)
            
            return access_token, refresh_token
            
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

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

    def generate_reset_code(self, email: str) -> dict:
        try:
            # Verificar si el usuario existe
            user = self.db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Generar código de restablecimiento
            reset_code = self.generate_verification_code()
            
            # Guardar el código en la base de datos
            user.verification_code = reset_code
            self.db.commit()
            self.db.refresh(user)
            
            # Enviar el código por correo
            email_sent = self.email_service.send_password_reset_code(email, reset_code)
            
            if not email_sent:
                return {
                    "message": "No se pudo enviar el correo de restablecimiento. Tu código es: " + reset_code,
                    "reset_code": reset_code
                }
            
            return {
                "message": "Se ha enviado un código de restablecimiento a tu correo electrónico",
                "reset_code": None
            }
            
        except HTTPException as he:
            raise he
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    def reset_password(self, email: str, new_password: str, reset_code: str) -> dict:
        try:
            # Verificar si el usuario existe
            user = self.db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Verificar si el código es correcto
            if user.verification_code != reset_code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Código de restablecimiento inválido"
                )
            
            # Hashear la nueva contraseña
            hashed_password = auth_handler.hash_password(new_password)
            
            # Actualizar la contraseña
            user.password = hashed_password
            user.verification_code = None  # Limpiar el código después de usarlo
            
            # Guardar los cambios
            self.db.commit()
            self.db.refresh(user)
            
            return {"message": "Contraseña restablecida exitosamente"}
            
        except HTTPException as he:
            raise he
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

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

    def enable_account(self, email: str) -> dict:
        try:
            # Verificar si el usuario existe
            user = self.db.query(UserModel).filter(UserModel.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Habilitar la cuenta
            user.status = True
            
            # Guardar los cambios
            self.db.commit()
            self.db.refresh(user)
            
            # Generar nuevos tokens con el estado actualizado
            access_token = auth_handler.encode_token(user)
            refresh_token = auth_handler.encode_refresh_token(user)
            
            return {
                "message": "Cuenta habilitada exitosamente",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            
        except HTTPException as he:
            raise he
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )