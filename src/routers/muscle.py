from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.muscle import Muscle
from src.models.muscle import Muscle as muscles
from src.repositories.muscle import MuscleRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler


muscle_router = APIRouter(tags=['Músculos'])

#CRUD muscle

@muscle_router.get('',response_model=List[Muscle],description="Devuelve todos los músculos")
def get_muscles(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[Muscle]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            result = MuscleRepository(db).get_all_muscles()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    
@muscle_router.get('/{id}',response_model=Muscle,description="Devuelve la información de un solo músculo")
def get_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> Muscle:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            element=  MuscleRepository(db).get_muscle_by_id(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested muscle was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content=jsonable_encoder(element),                        
                status_code=status.HTTP_200_OK
                )
        return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@muscle_router.post('',response_model=dict,description="Crea un nuevo músculo")
def create_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], muscle: Muscle = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            new_muscle = MuscleRepository(db).create_new_muscle(muscle)
            return JSONResponse(
                content={        
                "message": "The muscle was successfully created",        
                "data": jsonable_encoder(new_muscle)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@muscle_router.delete('/{id}',response_model=dict,description="Elimina un músculo específico")
def remove_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            element = MuscleRepository(db).delete_muscle(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested muscle was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@muscle_router.put('/{id}',response_model=dict,description="Actualiza un músculo específico")
def update_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), muscle: Muscle = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            element = MuscleRepository(db).update_muscle(id, muscle)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested muscle was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
