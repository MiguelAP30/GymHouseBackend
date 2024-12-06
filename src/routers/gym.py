from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.gym import Gym
from src.repositories.gym import GymRepository
from src.models.gym import Gym as gyms

gym_router = APIRouter(tags=['Gimnasios'])

#CRUD gym

@gym_router.get('/',response_model=List[Gym],description="Devuelve todos los gimnasios")
def get_gym(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[Gym]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = GymRepository(db).get_all_gym()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.post('/', response_model=Gym, description="Crea un nuevo gimnasio")
def create_gym(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], gym: Gym = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        current_user = payload.get("sub")
        
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        
        if status_user:
            existing_gym = GymRepository(db).get_gym_by_user(current_user)
            if existing_gym:
                return JSONResponse(content={"message": "You already have a gym created", "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
            
            new_gym = GymRepository(db).create_new_gym(gym)
            return JSONResponse(
                content={
                    "message": "The gym was successfully created",
                    "data": jsonable_encoder(new_gym)
                },
                status_code=status.HTTP_201_CREATED
            )
        
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.delete('/{id}',response_model=dict,description="Elimina un gimnasio específico")
def remove_gym(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            GymRepository(db).delete_gym(id)
            return JSONResponse(content={"message": "The gym was successfully deleted", "data": None}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.put('/{id}',response_model=Gym,description="Actualiza un gimnasio específico")
def update_gym(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), gym: Gym = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = GymRepository(db).update_gym(id, gym)
            return JSONResponse(content={"message": "The gym was successfully updated", "data": jsonable_encoder(result)}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.get('/{id}',response_model=Gym,description="Devuelve un gimnasio específico")
def get_gym_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = GymRepository(db).get_gym_by_id(id, current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

