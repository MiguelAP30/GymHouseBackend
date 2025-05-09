from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List, Optional
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.exercise_configuration import ExerciseConfiguration
from src.repositories.exercise_configuration import ExerciseConfigurationRepository
from src.models.exercise_configuration import ExerciseConfiguration as ExerciseConfigurationModel
from src.models.training_plan import TrainingPlan as TrainingPlanModel
from src.models.workout_day_exercise import WorkoutDayExercise as WorkoutDayExerciseModel

exercise_configuration_router = APIRouter(tags=['Configuraciones de ejercicios'])

#CRUD exercise_configuration

@exercise_configuration_router.get('',response_model=List[ExerciseConfiguration],description="Devuelve todas las configuraciones de ejercicios")
def get_exercise_configurations(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[ExerciseConfiguration]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = ExerciseConfigurationRepository(db).get_all_exercise_configurations()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@exercise_configuration_router.post('',response_model=dict,description="Crea una nueva configuración de ejercicio")
def create_exercise_configuration(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],exercise_configuration: ExerciseConfiguration = Body()) -> dict:
    db = SessionLocal()
    try:
        payload = auth_handler.decode_token(credentials.credentials)
        if not payload:
            return JSONResponse(content={"message": "Token inválido", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        current_user = payload.get("sub")
        if not status_user:
            return JSONResponse(content={"message": "Usuario inactivo", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        if role_user < 2:
            return JSONResponse(content={"message": "Privilegios insuficientes", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        # Lógica delegada al repositorio
        new_exercise_configuration = ExerciseConfigurationRepository(db).create_new_exercise_configuration(
            exercise_configuration,
            current_user
        )
        return JSONResponse(
            content={
                "message": "La configuración de ejercicio fue creada exitosamente",
                "data": jsonable_encoder(new_exercise_configuration)
            },
            status_code=status.HTTP_201_CREATED
        )
    except ValueError as ve:
        return JSONResponse(content={"message": str(ve), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content={"message": f"Error interno: {str(e)}", "data": None}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@exercise_configuration_router.delete('/{id}',response_model=dict,description="Elimina una configuración de ejercicio específica")
def remove_exercise_configuration(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    try:
        payload = auth_handler.decode_token(credentials.credentials)
        if not payload:
            return JSONResponse(content={"message": "Token inválido", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        current_user = payload.get("sub")
        if not status_user:
            return JSONResponse(content={"message": "Usuario inactivo", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        if role_user < 2:
            return JSONResponse(content={"message": "Privilegios insuficientes", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        deleted_data = ExerciseConfigurationRepository(db).delete_exercise_configuration(id, current_user)
        return JSONResponse(
            content={
                "message": "La configuración de ejercicio fue eliminada exitosamente",
                "data": jsonable_encoder(deleted_data)
            },
            status_code=status.HTTP_200_OK
        )
    except ValueError as ve:
        return JSONResponse(content={"message": str(ve), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content={"message": f"Error interno: {str(e)}", "data": None}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@exercise_configuration_router.get('/{id}',response_model=ExerciseConfiguration,description="Devuelve una configuración de ejercicio específica")
def get_exercise_configuration_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        # Obtener la configuración sin verificar permisos
        element = ExerciseConfigurationRepository(db).get_exercise_configuration_by_id(id)
        if not element:        
            return JSONResponse(
                content={            
                    "message": "La configuración de ejercicio solicitada no fue encontrada",            
                    "data": None        
                    }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
        return JSONResponse(
            content=jsonable_encoder(element),                        
            status_code=status.HTTP_200_OK
            )

@exercise_configuration_router.put('/{id}',response_model=dict,description="Actualiza una configuración de ejercicio específica")
def update_exercise_configuration(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],id: int = Path(ge=1),exercise_configuration: ExerciseConfiguration = Body()) -> dict:
    db = SessionLocal()
    try:
        payload = auth_handler.decode_token(credentials.credentials)
        if not payload:
            return JSONResponse(content={"message": "Token inválido", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        current_user = payload.get("sub")
        if not status_user:
            return JSONResponse(content={"message": "Usuario inactivo", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        if role_user < 2:
            return JSONResponse(content={"message": "Privilegios insuficientes", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        updated_data = ExerciseConfigurationRepository(db).update_exercise_configuration(id, exercise_configuration, current_user)
        return JSONResponse(
            content={
                "message": "La configuración de ejercicio fue actualizada exitosamente",
                "data": jsonable_encoder(updated_data)
            },
            status_code=status.HTTP_200_OK
        )
    except ValueError as ve:
        return JSONResponse(content={"message": str(ve), "data": None}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content={"message": f"Error interno: {str(e)}", "data": None}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
