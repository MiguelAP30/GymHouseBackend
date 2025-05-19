from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.history_pr_exercise import HistoryPrExercise, HistoryPrExerciseUpdate, FullHistoryPrExerciseCreate
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

@history_pr_exercise_router.post('',response_model=HistoryPrExercise,description="Crea un historial completo de PR de ejercicio incluyendo series y dropsets")
def create_history_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], full_data: FullHistoryPrExerciseCreate  = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if not payload:
        return JSONResponse(content={"message": "Token inválido", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    role_current_user = payload.get("user.role")
    status_user = payload.get("user.status")
    if role_current_user < 2:
        return JSONResponse(content={"message": "No tienes permisos", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    if not status_user:
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    current_user = payload.get("sub")
    try:
        repository = HistoryPrExerciseRepository(db)
        new_history = repository.create_new_history_pr_exercise(current_user, full_data)
        return JSONResponse(
            content={"message": "Entrenamiento completo creado exitosamente", "data": jsonable_encoder(new_history)},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Error al crear entrenamiento: {str(e)}", "data": None},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        db.close()

@history_pr_exercise_router.delete('/{id}', response_model=dict, description="Elimina un historial de PR de ejercicio específico")
def remove_history_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)

    if not payload:
        return JSONResponse(content={"message": "Token inválido"}, status_code=status.HTTP_401_UNAUTHORIZED)

    if payload.get("user.role") < 2:
        return JSONResponse(content={"message": "No tienes los permisos necesarios"}, status_code=status.HTTP_401_UNAUTHORIZED)

    if not payload.get("user.status"):
        return JSONResponse(content={"message": "Tu cuenta está inactiva"}, status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        current_user = payload.get("sub")
        result = HistoryPrExerciseRepository(db).remove_history_pr_exercise(id, current_user)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except ValueError as e:
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_404_NOT_FOUND)
    except PermissionError as e:
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_403_FORBIDDEN)

@history_pr_exercise_router.put('/{id}', response_model=HistoryPrExercise, description="Actualiza un historial de PR de ejercicio específico")
def update_history_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1), history_pr_exercise: HistoryPrExerciseUpdate = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)

    if not payload:
        return JSONResponse(content={"message": "Token inválido"}, status_code=status.HTTP_401_UNAUTHORIZED)

    if payload.get("user.role") < 2:
        return JSONResponse(content={"message": "No tienes los permisos necesarios"}, status_code=status.HTTP_401_UNAUTHORIZED)

    if not payload.get("user.status"):
        return JSONResponse(content={"message": "Tu cuenta está inactiva"}, status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        current_user = payload.get("sub")
        result = HistoryPrExerciseRepository(db).update_history_pr_exercise(id, history_pr_exercise, current_user)
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
    except ValueError as e:
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_404_NOT_FOUND)
    except PermissionError as e:
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_403_FORBIDDEN)

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

@history_pr_exercise_router.get('/user/{email}',response_model=List[HistoryPrExercise],description="Devuelve todos los historiales de PR de ejercicios de un usuario específico")
def get_history_pr_exercise_by_user_email(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], email: str = Path(min_length=5)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = HistoryPrExerciseRepository(db).get_history_pr_exercise_by_user_email(email)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@history_pr_exercise_router.get('/exercise/{id}/user/{email}',response_model=List[HistoryPrExercise],description="Devuelve todos los historiales de PR de ejercicios de un ejercicio específico de un usuario específico")
def get_history_pr_exercise_by_exercise_id_and_user_email(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), email: str = Path(min_length=5)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = HistoryPrExerciseRepository(db).get_history_pr_exercise_by_exercise_id_and_user_email(id, email)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

