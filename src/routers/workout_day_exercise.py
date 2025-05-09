from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.repositories.workout_day_exercise import WorkoutDayExerciseRepository
from src.schemas.workout_day_exercise import WorkoutDayExercise
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel
from src.models.training_plan import TrainingPlan as TrainingPlanModel
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

workout_day_exercise_router = APIRouter(tags=['Dias de entrenamiento'])

#CRUD workout_day_exercise

@workout_day_exercise_router.get('/my',response_model=List[WorkoutDayExercise],description="Devuelve todos mis entrenos por día de la semana")
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
        
@workout_day_exercise_router.get('/{id}',response_model=WorkoutDayExercise,description="Devuelve un entrenamiento específico por día de la semana")
def get_workout_day_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> WorkoutDayExercise:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            element=  WorkoutDayExerciseRepository(db).get_workout_day_exercise_by_id(id)
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

@workout_day_exercise_router.post('',response_model=dict,description="Crea un nuevo entrenamiento por día de la semana")
def create_workout_day_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], workoutDay: WorkoutDayExercise = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            try:
                new_excercise = WorkoutDayExerciseRepository(db).create_new_workout_day_exercise(workoutDay, current_user)
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
        elif not status_user:
            return JSONResponse(content={"message": "Usuario Inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios Insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@workout_day_exercise_router.delete('/{id}', response_model=dict, description="Elimina un entrenamiento específico por día de la semana")
def remove_workout_day_exercise(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1)
) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        current_user = payload.get("sub")
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            try:
                deleted_element = WorkoutDayExerciseRepository(db).delete_workout_day_exercise(id, current_user)
                return JSONResponse(
                    content={
                        "message": "El entrenamiento por día de la semana fue eliminado correctamente",
                        "data": jsonable_encoder(deleted_element)
                    },
                    status_code=status.HTTP_200_OK
                )
            except ValueError as e:
                return JSONResponse(
                    content={"message": str(e), "data": None},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        return JSONResponse(content={"message": "Privilegios Insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@workout_day_exercise_router.put('/{id}', response_model=dict, description="Actualiza un entrenamiento específico por día de la semana")
def update_workout_day_exercise(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    id: int = Path(ge=1),
    workoutDay: WorkoutDayExercise = Body()
) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        current_user = payload.get("sub")
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            try:
                updated_element = WorkoutDayExerciseRepository(db).update_workout_day_exercise(id, workoutDay, current_user)
                return JSONResponse(
                    content={
                        "message": "El entrenamiento por día de la semana fue actualizado correctamente",
                        "data": jsonable_encoder(updated_element)
                    },
                    status_code=status.HTTP_200_OK
                )
            except ValueError as e:
                return JSONResponse(
                    content={"message": str(e), "data": None},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
        elif not status_user:
            return JSONResponse(content={"message": "Usuario Inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        return JSONResponse(content={"message": "Privilegios Insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@workout_day_exercise_router.get('/training_plan/{training_plan_id}', response_model=List[WorkoutDayExercise], description="Devuelve todos los entrenamientos por día de la semana de un plan de entrenamiento específico")
def get_workout_day_exercises_by_training_plan(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    training_plan_id: int = Path(ge=1)
) -> List[WorkoutDayExercise]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = WorkoutDayExerciseRepository(db).get_workout_day_exercises_by_training_plan(training_plan_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios Insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)
