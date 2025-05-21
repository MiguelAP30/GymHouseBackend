from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.gym import Gym, GymUpdate, GymCreate
from src.repositories.gym import GymRepository
from src.models.gym import Gym as gyms

gym_router = APIRouter(tags=['Gimnasios'])

#CRUD gym

@gym_router.get('/by_user',response_model=Gym,description="Devuelve el gimnasio de un usuario específico")
def get_gym_by_user(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)]) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = GymRepository(db).get_gym_by_user(current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
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
            result = GymRepository(db).get_gym_by_id(id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.get('',response_model=List[Gym],description="Devuelve todos los gimnasios")
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

@gym_router.post('', response_model=Gym, description="Crea un nuevo gimnasio")
def create_gym(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], gym: GymCreate = Body()) -> dict:
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
            
            # Convertimos GymCreate a Gym agregando el user_email
            gym_data = gym.model_dump()
            gym_data['user_email'] = current_user
            gym_full = Gym(**gym_data)
            new_gym = GymRepository(db).create_new_gym(gym_full)
            return JSONResponse(
                content={
                    "message": "The gym was successfully created",
                    "data": jsonable_encoder(new_gym)
                },
                status_code=status.HTTP_201_CREATED
            )
        
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.delete('/admin/{id}',response_model=dict,description="Elimina un gimnasio específico (solo administradores)")
def remove_gym_admin(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user != 4:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            GymRepository(db).delete_gym_by_id(id)
            return JSONResponse(content={"message": "The gym was successfully deleted", "data": None}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.delete('/by_user',response_model=dict,description="Elimina el gimnasio del usuario actual")
def remove_gym_user(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)]) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            current_user = payload.get("sub")
            GymRepository(db).delete_gym_by_user(current_user)
            return JSONResponse(content={"message": "Your gym was successfully deleted", "data": None}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.put('/by_user',response_model=Gym,description="Actualiza el gimnasio del usuario actual")
def update_gym_user(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], gym: GymUpdate = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            current_user = payload.get("sub")
            # Convertimos GymUpdate a Gym agregando el user_email
            gym_data = gym.model_dump()
            gym_data['user_email'] = current_user
            gym_full = Gym(**gym_data)
            result = GymRepository(db).update_gym_by_user(current_user, gym_full)
            if result:
                return JSONResponse(content={"message": "Your gym was successfully updated", "data": jsonable_encoder(result)}, status_code=status.HTTP_200_OK)
            return JSONResponse(content={"message": "You don't have a gym to update", "data": None}, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@gym_router.put('/{gym_id}/max-users', response_model=dict, description="Aumenta el límite máximo de usuarios de un gimnasio")
def increase_max_users(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    gym_id: int = Path(ge=1),
    new_max_users: int = Query(ge=1, description="Nuevo límite máximo de usuarios")
) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 3:  # Solo gimnasios pueden aumentar su límite
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            try:
                result = GymRepository(db).increase_max_users(gym_id, new_max_users)
                return JSONResponse(content=result, status_code=status.HTTP_200_OK)
            except ValueError as e:
                return JSONResponse(content={"message": str(e), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)