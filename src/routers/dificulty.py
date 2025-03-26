from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.dificulty import Dificulty
from src.repositories.dificulty import DificultyRepository
from src.models.dificulty import Dificulty as dificulties

dificulty_router = APIRouter(tags=['Dificultades'])

#CRUD dificulty

@dificulty_router.get('',response_model=List[Dificulty],description="Devuelve todas las dificultades")
def get_dificulty(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[Dificulty]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = DificultyRepository(db).get_all_dificulty()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dificulty_router.post('',response_model=Dificulty,description="Crea una nueva dificultad")
def create_dificulty(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], dificulty: Dificulty = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_dificulty = DificultyRepository(db).create_new_dificulty(dificulty)
            return JSONResponse(
                content={        
                "message": "The dificulty was successfully created",        
                "data": jsonable_encoder(new_dificulty)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dificulty_router.delete('/{id}',response_model=dict,description="Elimina una dificultad específica")
def remove_dificulty(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = DificultyRepository(db).delete_dificulty(id)
            return JSONResponse(content={"message": "The dificulty was successfully deleted", "data": result}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dificulty_router.put('/{id}',response_model=Dificulty,description="Actualiza una dificultad específica")
def update_dificulty(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), dificulty: Dificulty = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = DificultyRepository(db).update_dificulty(id, dificulty)
            return JSONResponse(content={"message": "The dificulty was successfully updated", "data": result}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dificulty_router.get('/{id}',response_model=Dificulty,description="Devuelve una dificultad específica")
def get_dificulty_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = DificultyRepository(db).get_dificulty_by_id(id)
            return JSONResponse(content={"message": "The dificulty was successfully found", "data": jsonable_encoder(result)}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dificulty_router.post('/init', response_model=dict, description="Inicializa dificultades específicas en la base de datos")
def init_dificulty(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)]) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            dificulty_data = [
                {"name": "Facil"},
                {"name": "Medio"},
                {"name": "Dificil"},
                {"name": "Dificil"}
            ]
            
            created_dificulties = []
            for dificulty in dificulty_data:
                if not db.query(dificulties).filter_by(name=dificulty["name"]).first():
                    new_dificulty = dificulties(**dificulty)
                    db.add(new_dificulty)
                    created_dificulties.append(new_dificulty)
            
            db.commit()
            return JSONResponse(
                content={
                    "message": "Las dificultades se han inicializado correctamente",
                    "data": jsonable_encoder(created_dificulties)
                },
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

