from fastapi import APIRouter, Body, Depends, Query, Path, Security, status, HTTPException
from fastapi.responses import JSONResponse 
from typing import Annotated, List 
from fastapi.security import HTTPAuthorizationCredentials 
from fastapi.encoders import jsonable_encoder 
from src.repositories.user import UserRepository 
from src.repositories.auth import AuthRepository 
from src.config.database import SessionLocal 
from src.schemas.user import (
    User as UserCreateSchema,
    UserLogin as UserLoginSchema,
    ChangePassword,
    ResetPassword
)
from src.auth.has_access import has_access, security    
from src.auth import auth_handler
import traceback

auth_router = APIRouter()

@auth_router.post("/verify_email", tags=["Autorización"], response_model=dict, description="Verificar el email del usuario")
def verify_email(email: str = Body(...), verification_code: str = Body(...)) -> dict:
    try:
        auth_repo = AuthRepository()
        result = auth_repo.verify_email(email, verification_code)
        return result
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error al verificar email: {str(e)}")
        print(f"Detalles del error: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@auth_router.post("/register", tags=["Autorización"], response_model=dict, description="Registrar un nuevo usuario") 
def register_user(user: UserCreateSchema = Body()) -> dict: 
    try: 
        auth_repo = AuthRepository()
        new_user = auth_repo.register_user(user) 
        # Obtener el mensaje del objeto de usuario
        message = getattr(new_user, 'message', "Usuario registrado exitosamente. Por favor verifica tu email.")
        
        # Convertir el objeto a diccionario para la respuesta
        user_dict = jsonable_encoder(new_user)
        
        return JSONResponse( 
            content={ 
                "message": message, 
                "data": user_dict,
                }, 
                status_code=status.HTTP_201_CREATED, 
            ) 
    except HTTPException as he:
        raise he
    except Exception as err:
        error_details = traceback.format_exc()
        print(f"Error al registrar usuario: {str(err)}")
        print(f"Detalles del error: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

@auth_router.post("/login", tags=["Autorización"], response_model=dict, description="Autenticar un usuario") 
def login_user(user: UserLoginSchema) -> dict: 
    try:
        db = SessionLocal()
        check_user = UserRepository(db).get_user_by_email(email=user.email)
        
        if check_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
            
        if not check_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Por favor verifica tu email antes de iniciar sesión"
            )
            
        access_token, refresh_token = AuthRepository().login_user(user)
        return JSONResponse(
            content={
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status_code=status.HTTP_200_OK,
        )
    except HTTPException as e:
        return JSONResponse(
            content={"message": e.detail},
            status_code=e.status_code,
        )
    except Exception as e:
        return JSONResponse(
            content={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@auth_router.get("/refresh_token", tags=["Autorización"], response_model=dict, description="Crear un nuevo token con tiempo de vida extendido") 
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict: 
    refresh_token = credentials.credentials 
    new_token = auth_handler.refresh_token(refresh_token) 
    return {"access_token": new_token}


@auth_router.get("/user_data", tags=["Autorización"], response_model=dict, description="Obtener datos del usuario a partir de su token")
def get_user_data(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    try:
        # Obtener el token desde las credenciales
        token = credentials.credentials

        # Decodificar el token para obtener la información del usuario
        user_data = auth_handler.decode_token(token)

        print(user_data)

        if user_data:
            return {"message": "User found", "data": jsonable_encoder(user_data)}
        else:
            return {"message": "User not found", "data": None}
        
    except Exception as err:
        return {"message": str(err), "data": None}

@auth_router.post("/change_password", tags=["Autorización"], response_model=dict, description="Cambiar la contraseña del usuario autenticado")
def change_password(
    credentials: HTTPAuthorizationCredentials = Security(security),
    password_data: ChangePassword = Body()
) -> dict:
    try:
        user_data = auth_handler.decode_token(credentials.credentials)
        email = user_data.get("sub")
        result = AuthRepository().change_password(
            email=email,
            current_password=password_data.current_password,
            new_password=password_data.new_password
        )
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as err:
        return JSONResponse(
            content={"message": str(err)},
            status_code=status.HTTP_400_BAD_REQUEST
        )

@auth_router.post("/forgot_password", tags=["Autorización"], response_model=dict, description="Solicitar código para restablecer contraseña")
def forgot_password(email: str = Body(...)) -> dict:
    try:
        auth_repo = AuthRepository()
        result = auth_repo.generate_reset_code(email)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as he:
        raise he
    except Exception as err:
        error_details = traceback.format_exc()
        print(f"Error al solicitar código de restablecimiento: {str(err)}")
        print(f"Detalles del error: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

@auth_router.post("/reset_password", tags=["Autorización"], response_model=dict, description="Restablecer la contraseña usando el código")
def reset_password(password_data: ResetPassword = Body()) -> dict:
    try:
        auth_repo = AuthRepository()
        result = auth_repo.reset_password(
            email=password_data.email,
            new_password=password_data.new_password,
            reset_code=password_data.reset_code
        )
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as he:
        raise he
    except Exception as err:
        error_details = traceback.format_exc()
        print(f"Error al restablecer contraseña: {str(err)}")
        print(f"Detalles del error: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

@auth_router.post("/resend-verification", tags=["Autorización"], response_model=dict, description="Reenviar el código de verificación al correo del usuario")
def resend_verification_code(email: str = Body(...)) -> dict:
    try:
        auth_repo = AuthRepository()
        result = auth_repo.resend_verification_code(email)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except HTTPException as he:
        raise he
    except Exception as err:
        error_details = traceback.format_exc()
        print(f"Error al reenviar código de verificación: {str(err)}")
        print(f"Detalles del error: {error_details}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )
