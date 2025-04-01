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

auth_router = APIRouter()

@auth_router.post( "/register", tags=["Autorización"], response_model=dict, description="Registrar un nuevo usuario") 
def register_user(user: UserCreateSchema = Body()) -> dict: 
    try: 
        new_user = AuthRepository().register_user(user) 
        return JSONResponse( 
            content={ 
                "message": "The user was successfully registered", 
                "data": jsonable_encoder(new_user),
                }, 
                status_code=status.HTTP_201_CREATED, 
            ) 
    except Exception as err: 
        return JSONResponse( 
            content={"message": str(err), "data": None}, 
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        )

@auth_router.post("/login",tags=["Autorización"], response_model=dict, description="Autenticar un usuario") 
def login_user(user: UserLoginSchema) -> dict: 
    try:
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

@auth_router.post("/forgot_password", tags=["Autorización"], response_model=dict, description="Solicitar token para restablecer contraseña")
def forgot_password(email: str = Body(...)) -> dict:
    try:
        result = AuthRepository().generate_reset_token(email)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as err:
        return JSONResponse(
            content={"message": str(err)},
            status_code=status.HTTP_400_BAD_REQUEST
        )

@auth_router.post("/reset_password", tags=["Autorización"], response_model=dict, description="Restablecer la contraseña usando el token")
def reset_password(password_data: ResetPassword = Body()) -> dict:
    try:
        result = AuthRepository().reset_password(
            email=password_data.email,
            new_password=password_data.new_password,
            reset_token=password_data.reset_token
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
