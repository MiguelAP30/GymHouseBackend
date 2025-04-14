from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.repositories.workout_day_exercise import WorkoutDayExerciseRepository
from src.schemas.workout_day_exercise import WorkoutDayExercise
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

workout_day_exercise_router = APIRouter(tags=['Ejercicios para días de la semana'])

#CRUD workout_day_exercise

@workout_day_exercise_router.get('/my',response_model=List[WorkoutDayExercise],description="Devuelve todos mis ejercicios por día de la semana")
def get_all_my_workout_day_exercises(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[WorkoutDayExercise]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            result = WorkoutDayExerciseRepository(db).get_all_my_workout_day_exercises(current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)
        
@workout_day_exercise_router.get('/premium',response_model=List[WorkoutDayExercise],description="Devuelve todos los ejercicios de usuarios premium por dia de la semana")
def get_premium_workout_day_exercises(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[WorkoutDayExercise]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = WorkoutDayExerciseRepository(db).get_premium_workout_day_exercises()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)
        
@workout_day_exercise_router.get('/gym',response_model=List[WorkoutDayExercise],description="Devuelve todos los ejercicios de usuarios gimnasio por día de la semana")
def get_gym_workout_day_exercises(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[WorkoutDayExercise]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = WorkoutDayExerciseRepository(db).get_gym_workout_day_exercises()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)
            
@workout_day_exercise_router.get('/admin',response_model=List[WorkoutDayExercise],description="Devuelve todos los ejercicios de usuarios administradores por día de la semana")
def get_admin_workout_day_exercises(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[WorkoutDayExercise]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = WorkoutDayExerciseRepository(db).get_admin_workout_day_exercises()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)

@workout_day_exercise_router.get('/{id}',response_model=WorkoutDayExercise,description="Devuelve un ejercicio específico por día de la semana")
def get_workout_day_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> WorkoutDayExercise:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            element=  WorkoutDayExerciseRepository(db).get_workout_day_exercise_by_id(id, current_user)
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

@workout_day_exercise_router.post('',response_model=dict,description="Crea un nuevo ejercicio por día de la semana")
def create_workout_day_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], exercise: WorkoutDayExercise = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            try:
                new_excercise = WorkoutDayExerciseRepository(db).create_new_workout_day_exercise(exercise)
                return JSONResponse(
                    content={        
                    "message": "The exercise per week day was successfully created",        
                    "data": jsonable_encoder(new_excercise)    
                    }, 
                    status_code=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return JSONResponse(
                    content={
                        "message": str(e),
                        "data": None
                    },
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                return JSONResponse(
                    content={
                        "message": f"Error al crear el ejercicio: {str(e)}",
                        "data": None
                    },
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)

@workout_day_exercise_router.delete('/{id}',response_model=dict,description="Elimina un ejercicio específico por día de la semana")
def remove_workout_day_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            element = WorkoutDayExerciseRepository(db).delete_workout_day_exercise(id, current_user)  
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
