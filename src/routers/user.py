from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.user import User, UpdateUser, SubscriptionConfirmation
from src.models.user import User as users
from src.repositories.user import UserRepository
from datetime import date

from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

user_router = APIRouter(tags=['Usuarios'])

#CRUD user

@user_router.get('',response_model=List[User],description="Devuelve todos los usuarios")
def get_users(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[User]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        if role_current_user != 4:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        result = UserRepository(db).get_all_users()
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@user_router.put('/{email}',response_model=dict,description="Updates specific user")
def update_user(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], email: str = Path(min_length=5), user: UpdateUser = Body()) -> dict:
    payload = auth_handler.decode_token(credentials.credentials)
    db = SessionLocal()
    if payload:
        element = UserRepository(db).update_user(email, user)
        if not element:        
            return JSONResponse(
                content={            
                    "message": "The requested user was not found",            
                    "data": None        
                    }, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_router.get('/{email}',response_model=User,description="Devuelve la información de un solo usuario")
def get_user(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], email: str = Path(min_length=5)) -> User:
    db = SessionLocal()
    element=  UserRepository(db).get_user_by_email(email)
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        if role_current_user < 1:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if not element:        
            return JSONResponse(
                content={            
                    "message": "The requested user was not found",            
                    "data": None        
                    }, 
                status_code=status.HTTP_404_NOT_FOUND
                )    
        return JSONResponse(
            content=jsonable_encoder(element),                        
            status_code=status.HTTP_200_OK
        )

@user_router.put('/delete/{email}',response_model=dict,description="Desactiva el usuario del sistema")
def remove_user(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], email: str = Path(min_length=5)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        element = UserRepository(db).delete_user(email)
        if not element:        
            return JSONResponse(
                content={            
                    "message": "The requested user was not found",            
                    "data": None        
                    }, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_router.put('/role/{email}',response_model=dict,description="Actualiza el rol del usuario en el sistema")
def update_role(
    credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], 
    email: str = Path(min_length=5), 
    role_id: int = Query(...),
    final_date: date = Query(..., description="Fecha de finalización del rol")
) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user > 3:
            if status_user:
                element = UserRepository(db).update_role(email, role_id, final_date)
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if not element:        
            return JSONResponse(
                content={            
                    "message": "The requested user was not found",            
                    "data": None        
                    }, 
                status_code=status.HTTP_404_NOT_FOUND
            )
        return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_router.put('/verification/{email}', response_model=dict, description="Actualiza el estado de verificación de un usuario")
def update_verification_status(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], 
    email: str = Path(min_length=5), 
    is_verified: bool = Query(..., description="Nuevo estado de verificación")
) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user == 4:  # Solo administradores (role_id = 4)
            if status_user:
                element = UserRepository(db).update_verification_status(email, is_verified)
                if not element:
                    return JSONResponse(
                        content={
                            "message": "El usuario solicitado no fue encontrado",
                            "data": None
                        },
                        status_code=status.HTTP_404_NOT_FOUND
                    )
                return JSONResponse(
                    content={
                        "message": "Estado de verificación actualizado correctamente",
                        "data": jsonable_encoder(element)
                    },
                    status_code=status.HTTP_200_OK
                )
            else:
                return JSONResponse(
                    content={"message": "Tu cuenta está inactiva", "data": None},
                    status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={"message": "No tienes los permisos necesarios", "data": None},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    return JSONResponse(
        content={"message": "No tienes los permisos necesarios", "data": None},
        status_code=status.HTTP_401_UNAUTHORIZED
    )

@user_router.post('/subscription/confirm', response_model=dict, description="Confirma una suscripción y actualiza el rol del usuario")
def confirm_subscription(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    subscription_data: SubscriptionConfirmation = Body(...)
) -> dict:
    """
    Endpoint para confirmar una suscripción.
    """
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    
    if payload:
        role_user = payload.get("user.role")
        if role_user != 4:  # Solo administradores pueden confirmar suscripciones
            return JSONResponse(
                content={"message": "No tienes los permisos necesarios", "data": None},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
            
        try:
            # Aquí podrías agregar lógica para verificar el payment_id con tu pasarela de pago
            # Por ejemplo, hacer una llamada a la API de la pasarela para verificar el pago
            
            # Actualizar el rol y fechas del usuario
            element = UserRepository(db).update_role(
                email=subscription_data.email,
                role_id=subscription_data.role_id,
                final_date=subscription_data.final_date
            )
            
            if not element:
                return JSONResponse(
                    content={"message": "Usuario no encontrado", "data": None},
                    status_code=status.HTTP_404_NOT_FOUND
                )
                
            return JSONResponse(
                content={
                    "message": "Suscripción confirmada exitosamente",
                    "data": jsonable_encoder(element)
                },
                status_code=status.HTTP_200_OK
            )
            
        except Exception as e:
            return JSONResponse(
                content={"message": f"Error al confirmar la suscripción: {str(e)}", "data": None},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    return JSONResponse(
        content={"message": "No tienes los permisos necesarios", "data": None},
        status_code=status.HTTP_401_UNAUTHORIZED
    )

