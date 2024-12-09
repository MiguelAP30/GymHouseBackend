from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.repositories.exercise_per_week_day import ExercisePerWeekDayRepository
from src.schemas.exercise_per_week_day import ExercisePerWeekDay
from src.models.exercise_per_week_day import ExercisePerWeekDay as ExercisePerWeekDayModel
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

exercise_per_week_day_router = APIRouter(tags=['Ejercicios para días de la semana'])

#CRUD exercise_per_week_day

@exercise_per_week_day_router.get('',response_model=List[ExercisePerWeekDay],description="Devuelve todos mis ejercicios por día de la semana")
def get_all_my_excercise_per_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[ExercisePerWeekDay]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            result = ExercisePerWeekDayRepository(db).get_all_my_excercise_per_week_day(current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)
        
@exercise_per_week_day_router.get('',response_model=List[ExercisePerWeekDay],description="Devuelve todos los ejercicios de usuarios premium por dia de la semana")
def get_premium_excercise_per_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[ExercisePerWeekDay]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExercisePerWeekDayRepository(db).get_premium_excercise_per_week_day()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)
        
@exercise_per_week_day_router.get('',response_model=List[ExercisePerWeekDay],description="Devuelve todos los ejercicios de clientes por día de la semana")
def get_client_excercise_per_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[ExercisePerWeekDay]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExercisePerWeekDayRepository(db).get_client_excercise_per_week_day()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)
        
@exercise_per_week_day_router.get('',response_model=List[ExercisePerWeekDay],description="Devuelve todos los ejercicios de administradores por día de la semana")
def get_admin_excercise_per_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[ExercisePerWeekDay]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExercisePerWeekDayRepository(db).get_admin_excercise_per_week_day()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)

@exercise_per_week_day_router.get('/{id}',response_model=ExercisePerWeekDay,description="Devuelve un ejercicio específico por día de la semana")
def get_excercise_per_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> ExercisePerWeekDay:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            element=  ExercisePerWeekDayRepository(db).get_excercise_per_week_day_by_id(id, current_user)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested exercise per week day was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content=jsonable_encoder(element),                        
                status_code=status.HTTP_200_OK
                )
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)

@exercise_per_week_day_router.post('',response_model=dict,description="Crea un nuevo ejercicio por día de la semana")
def create_excercise_per_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], exercise: ExercisePerWeekDay = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            new_excercise = ExercisePerWeekDayRepository(db).create_new_excercise_per_week_day(exercise)
            return JSONResponse(
                content={        
                "message": "The exercise per week day was successfully created",        
                "data": jsonable_encoder(new_excercise)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)

@exercise_per_week_day_router.delete('/{id}',response_model=dict,description="Elimina un ejercicio específico por día de la semana")
def remove_excercise_per_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            element = ExercisePerWeekDayRepository(db).delete_excercise_per_week_day(id, current_user)  
            return JSONResponse(
                content={        
                    "message": "The exercise per week day was successfully removed",        
                    "data": jsonable_encoder(element)    
                }, 
                status_code=status.HTTP_200_OK
            )
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)
