from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.specific_muscle import SpecificMuscle
from src.repositories.specific_muscle import SpecificMuscleRepository
from src.models.specific_muscle import SpecificMuscle as specific_muscle

specific_muscle_router = APIRouter(tags=['SpecificMuscle'])

#CRUD specific_muscle

@specific_muscle_router.get('/',response_model=List[SpecificMuscle],description="Devuelve todos los músculos específicos")
def get_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[SpecificMuscle]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = SpecificMuscleRepository(db).get_all_specific_muscle()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.post('/',response_model=SpecificMuscle,description="Crea un nuevo músculo específico")
def create_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], specific_muscle: SpecificMuscle = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_specific_muscle = SpecificMuscleRepository(db).create_new_specific_muscle(specific_muscle)
            return JSONResponse(
                content={        
                "message": "The specific_muscle was successfully created",        
                "data": jsonable_encoder(new_specific_muscle)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.delete('/{id}',response_model=dict,description="Elimina un músculo específico específico")
def remove_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            SpecificMuscleRepository(db).delete_specific_muscle(id)
            return JSONResponse(content={"message": "The specific_muscle was successfully deleted", "data": None}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.put('/{id}',response_model=SpecificMuscle,description="Actualiza un músculo específico específico")
def update_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), specific_muscle: SpecificMuscle = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            updated_specific_muscle = SpecificMuscleRepository(db).update_specific_muscle(id, specific_muscle)
            return JSONResponse(
                content={        
                "message": "The specific_muscle was successfully updated",        
                "data": jsonable_encoder(updated_specific_muscle)    
                }, 
                status_code=status.HTTP_200_OK
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.get('/{id}',response_model=SpecificMuscle,description="Devuelve un músculo específico específico")
def get_specific_muscle_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = SpecificMuscleRepository(db).get_specific_muscle_by_id(id)
            return JSONResponse(content={"message": "The specific_muscle was successfully obtained", "data": jsonable_encoder(result)}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

