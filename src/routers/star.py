from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.star import Star
from src.repositories.star import StarRepository
from src.models.star import Star as star

star_router = APIRouter(tags=['Star'])

#CRUD star

@star_router.get('',response_model=List[Star],description="Devuelve todas las estrellas")
def get_star(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[Star]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = StarRepository(db).get_all_star()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@star_router.post('',response_model=Star,description="Crea una nueva estrella")
def create_star(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], star: Star = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_star = StarRepository(db).create_new_star(star)
            return JSONResponse(
                content={        
                "message": "The star was successfully created",        
                "data": jsonable_encoder(new_star)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@star_router.delete('/{id}',response_model=dict,description="Elimina una estrella específica")
def remove_star(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = StarRepository(db).delete_star(id)
            return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@star_router.put('/{id}',response_model=Star,description="Actualiza una estrella específica")
def update_star(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), star: Star = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = StarRepository(db).update_star(id,star)
            return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@star_router.get('/{id}',response_model=Star,description="Devuelve una estrella específica")
def get_star_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = StarRepository(db).get_star_by_id(id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@star_router.get('/training_plan/{training_plan_id}', response_model=List[Star], description="Devuelve todas las estrellas de un plan de entrenamiento específico")
def get_stars_by_training_plan(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], training_plan_id: int = Path(ge=1)) -> List[Star]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = StarRepository(db).get_stars_by_training_plan(training_plan_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)