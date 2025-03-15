from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.user import User
from src.models.user import User as users
from src.repositories.user import UserRepository

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

@user_router.put('/{email}',response_model=dict,description="Desactiva el usuario del sistema")
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

@user_router.put('/user_role/{email}',response_model=dict,description="Actualiza el rol del usuario en el sistema")
def update_role(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], email: str = Path(min_length=5), role_id: int = Query(...)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        element = UserRepository(db).update_role(email, role_id)
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

# @user_router.put('/{email}',response_model=dict,description="Updates specific user")
# def update_user(email: str = Path(min_length=5), user: User = Body()) -> dict:
#     db = SessionLocal()
#     element = UserRepository(db).update_user(email, user)
#     if not element:        
#         return JSONResponse(
#             content={            
#                 "message": "The requested user was not found",            
#                 "data": None        
#                 }, 
#             status_code=status.HTTP_404_NOT_FOUND
#         )
#     return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)