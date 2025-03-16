from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.series_pr_exercise import SeriesPrExercise
from src.repositories.series_pr_exercise import SeriesPrExerciseRepository

series_pr_exercise_router = APIRouter(tags=['Series PR de ejercicios'])

@series_pr_exercise_router.get('', response_model=List[SeriesPrExercise], description="Devuelve todas las series PR de ejercicios de un historial")
def get_series_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], history_pr_exercise_id: int = Query(ge=1)) -> List[SeriesPrExercise]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = SeriesPrExerciseRepository(db).get_all_series_pr_exercise(history_pr_exercise_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@series_pr_exercise_router.post('', response_model=SeriesPrExercise, description="Crea una nueva serie PR de ejercicio")
def create_series_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], series_pr_exercise: SeriesPrExercise = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = SeriesPrExerciseRepository(db).create_new_series_pr_exercise(series_pr_exercise)
            return JSONResponse(
                content={
                    "message": "La serie PR de ejercicio fue creada exitosamente",
                    "data": jsonable_encoder(result)
                },
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@series_pr_exercise_router.delete('/{id}', response_model=dict, description="Elimina una serie PR de ejercicio específica")
def remove_series_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = SeriesPrExerciseRepository(db).remove_series_pr_exercise(id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@series_pr_exercise_router.get('/{id}', response_model=SeriesPrExercise, description="Devuelve una serie PR de ejercicio específica")
def get_series_pr_exercise_by_id(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = SeriesPrExerciseRepository(db).get_series_pr_exercise_by_id(id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@series_pr_exercise_router.put('/{id}', response_model=SeriesPrExercise, description="Actualiza una serie PR de ejercicio específica")
def update_series_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1), series_pr_exercise: SeriesPrExercise = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = SeriesPrExerciseRepository(db).update_series_pr_exercise(id, series_pr_exercise)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED) 