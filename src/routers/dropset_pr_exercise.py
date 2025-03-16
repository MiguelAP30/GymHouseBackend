from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.dropset_pr_exercise import DropSetPrExercise
from src.repositories.dropset_pr_exercise import DropSetPrExerciseRepository

dropset_pr_exercise_router = APIRouter(tags=['Dropsets PR de ejercicios'])

@dropset_pr_exercise_router.get('', response_model=List[DropSetPrExercise], description="Devuelve todos los dropsets PR de ejercicios de una serie")
def get_dropset_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], serie_pr_exercise_id: int = Query(ge=1)) -> List[DropSetPrExercise]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = DropSetPrExerciseRepository(db).get_all_dropset_pr_exercise(serie_pr_exercise_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dropset_pr_exercise_router.post('', response_model=DropSetPrExercise, description="Crea un nuevo dropset PR de ejercicio")
def create_dropset_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], dropset_pr_exercise: DropSetPrExercise = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = DropSetPrExerciseRepository(db).create_new_dropset_pr_exercise(dropset_pr_exercise)
            return JSONResponse(
                content={
                    "message": "El dropset PR de ejercicio fue creado exitosamente",
                    "data": jsonable_encoder(result)
                },
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dropset_pr_exercise_router.delete('/{id}', response_model=dict, description="Elimina un dropset PR de ejercicio específico")
def remove_dropset_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = DropSetPrExerciseRepository(db).remove_dropset_pr_exercise(id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dropset_pr_exercise_router.get('/{id}', response_model=DropSetPrExercise, description="Devuelve un dropset PR de ejercicio específico")
def get_dropset_pr_exercise_by_id(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = DropSetPrExerciseRepository(db).get_dropset_pr_exercise_by_id(id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@dropset_pr_exercise_router.put('/{id}', response_model=DropSetPrExercise, description="Actualiza un dropset PR de ejercicio específico")
def update_dropset_pr_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1), dropset_pr_exercise: DropSetPrExercise = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = DropSetPrExerciseRepository(db).update_dropset_pr_exercise(id, dropset_pr_exercise)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED) 