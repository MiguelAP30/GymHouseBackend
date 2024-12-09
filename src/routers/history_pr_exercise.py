from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.history_pr_exercise import HistoryPrExercise
from src.repositories.history_pr_exercise import HistoryPrExerciseRepository
from src.models.history_pr_exercise import HistoryPrExercise as history_pr_exercises

history_pr_exercise_router = APIRouter(tags=['Historial de PR de ejercicios'])

#CRUD history_pr_exercise

@history_pr_exercise_router.get('',response_model=List[HistoryPrExercise],description="Devuelve todos los historiales de PR de ejercicios")
def get_history_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[HistoryPrExercise]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = HistoryPrExerciseRepository(db).get_all_history_pr_exercise(current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.post('',response_model=HistoryPrExercise,description="Crea un nuevo historial de PR de ejercicio")
def create_history_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], history_pr_exercise: HistoryPrExercise = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_history_pr_exercise = HistoryPrExerciseRepository(db).create_new_history_pr_exercise(history_pr_exercise)
            return JSONResponse(
                content={        
                "message": "The history pr exercise was successfully created",        
                "data": jsonable_encoder(new_history_pr_exercise)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.delete('/{id}',response_model=dict,description="Elimina un historial de PR de ejercicio específico")
def remove_history_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = HistoryPrExerciseRepository(db).remove_history_pr_exercise(id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.put('/{id}',response_model=HistoryPrExercise,description="Actualiza un historial de PR de ejercicio específico")
def update_history_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), history_pr_exercise: HistoryPrExercise = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = HistoryPrExerciseRepository(db).update_history_pr_exercise(id, history_pr_exercise)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.get('/{id}',response_model=HistoryPrExercise,description="Devuelve un historial de PR de ejercicio específico")
def get_history_pr_exercise_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = HistoryPrExerciseRepository(db).get_history_pr_exercise_by_id(id, current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.get('/exercise/{id}',response_model=List[HistoryPrExercise],description="Devuelve todos los historiales de PR de ejercicios de un ejercicio específico")
def get_history_pr_exercise_by_exercise_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = HistoryPrExerciseRepository(db).get_history_pr_exercise_by_exercise_id(id, current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.get('/user/{id}',response_model=List[HistoryPrExercise],description="Devuelve todos los historiales de PR de ejercicios de un usuario específico")
def get_history_pr_exercise_by_user_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = HistoryPrExerciseRepository(db).get_history_pr_exercise_by_user_id(id, current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.get('/exercise/{id}/user/{id_user}',response_model=List[HistoryPrExercise],description="Devuelve todos los historiales de PR de ejercicios de un ejercicio específico de un usuario específico")
def get_history_pr_exercise_by_exercise_id_and_user_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), id_user: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = HistoryPrExerciseRepository(db).get_history_pr_exercise_by_exercise_id_and_user_id(id, id_user, current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

