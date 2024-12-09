from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.user_gym import UserGym
from src.repositories.user_gym import UserGymRepository
from src.models.user_gym import UserGym as user_gym

user_gym_router = APIRouter(tags=['UserGym'])

#CRUD user_gym

@user_gym_router.get('',response_model=List[UserGym],description="Devuelve todos los usuarios de un gimnasio")
def get_user_gym(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[UserGym]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = UserGymRepository(db).get_all_user_gym(current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_gym_router.post('',response_model=UserGym,description="Crea un nuevo usuario de un gimnasio")
def create_user_gym(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], user_gym: UserGym = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_user_gym = UserGymRepository(db).create_new_user_gym(user_gym)
            return JSONResponse(
                content={        
                "message": "The user_gym was successfully created",        
                "data": jsonable_encoder(new_user_gym)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_gym_router.delete('/{id}',response_model=dict,description="Elimina un usuario de un gimnasio específico")
def remove_user_gym(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            UserGymRepository(db).delete_user_gym(id)
            return JSONResponse(content={"message": "The user_gym was successfully deleted", "data": None}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_gym_router.put('/{id}',response_model=UserGym,description="Actualiza un usuario de un gimnasio específico")
def update_user_gym(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), user_gym: UserGym = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = UserGymRepository(db).update_user_gym(id, user_gym)
            return JSONResponse(content={"message": "The user_gym was successfully updated", "data": jsonable_encoder(result)}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@user_gym_router.get('/{id}',response_model=UserGym,description="Devuelve un usuario de un gimnasio específico")
def get_user_gym_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = UserGymRepository(db).get_user_gym_by_id(id)
            return JSONResponse(content={"message": "The user_gym was successfully found", "data": jsonable_encoder(result)}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

