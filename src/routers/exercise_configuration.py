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
def create_exercise_configuration(
    credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], 
    exercise_configuration: ExerciseConfiguration = Body()
) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            try:
                new_exercise_configuration = ExerciseConfigurationRepository(db).create_new_exercise_configuration(
                    exercise_configuration,
                    current_user
                )
                return JSONResponse(
                    content={        
                    "message": "The exercise configuration was successfully created",        
                    "data": jsonable_encoder(new_exercise_configuration)    
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
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)

@exercise_configuration_router.delete('/{id}',response_model=dict,description="Elimina una configuración de ejercicio específica")
def remove_exercise_configuration(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            # Verificar que la configuración pertenece al usuario actual o es administrador
            element = ExerciseConfigurationRepository(db).get_exercise_configuration_by_id(id)
            if not element:
                return JSONResponse(
                    content={            
                        "message": "The requested exercise configuration was not found",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            
            # Verificar que el plan de entrenamiento pertenece al usuario actual o es administrador
            workout_day_exercise = db.query(WorkoutDayExerciseModel).filter(WorkoutDayExerciseModel.id == element.workout_day_exercise_id).first()
            if not workout_day_exercise:
                return JSONResponse(
                    content={            
                        "message": "El ejercicio por día de la semana asociado no fue encontrado",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            
            training_plan = db.query(TrainingPlanModel).filter(TrainingPlanModel.id == workout_day_exercise.training_plan_id).first()
            if not training_plan:
                return JSONResponse(
                    content={            
                        "message": "El plan de entrenamiento asociado no fue encontrado",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
                    
            if training_plan.user_email != current_user and role_user != 4:
                return JSONResponse(
                    content={            
                        "message": "You do not have permission to delete this exercise configuration",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_403_FORBIDDEN
                    )
                
            element = ExerciseConfigurationRepository(db).delete_exercise_configuration(id)  
            return JSONResponse(
                content={        
                    "message": "The exercise configuration was successfully deleted",        
                    "data": jsonable_encoder(element)    
                }, 
                status_code=status.HTTP_200_OK
            )
        elif not status_user:
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)

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
def update_exercise_configuration(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), exercise_configuration: ExerciseConfiguration = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            # Verificar que la configuración existe
            element = ExerciseConfigurationRepository(db).get_exercise_configuration_by_id(id)
            if not element:
                return JSONResponse(
                    content={            
                        "message": "The requested exercise configuration was not found",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            
            # Obtener el workout day exercise actual y verificar permisos
            current_workout_day_exercise = db.query(WorkoutDayExerciseModel).filter(
                WorkoutDayExerciseModel.id == element.workout_day_exercise_id
            ).first()
            
            if not current_workout_day_exercise:
                return JSONResponse(
                    content={            
                        "message": "El ejercicio por día de la semana asociado no fue encontrado",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            
            # Obtener el plan de entrenamiento actual
            current_training_plan = db.query(TrainingPlanModel).filter(
                TrainingPlanModel.id == current_workout_day_exercise.training_plan_id
            ).first()
            
            if not current_training_plan:
                return JSONResponse(
                    content={            
                        "message": "El plan de entrenamiento asociado no fue encontrado",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            
            # Verificar que el usuario tiene permiso para modificar esta configuración
            if current_training_plan.user_email != current_user and role_user != 4:
                return JSONResponse(
                    content={            
                        "message": "You do not have permission to update this exercise configuration",            
                        "data": None        
                        }, 
                        status_code=status.HTTP_403_FORBIDDEN
                    )
            
            # Si se está cambiando el workout_day_exercise_id, verificar que el nuevo pertenece al usuario
            if exercise_configuration.workout_day_exercise_id != element.workout_day_exercise_id:
                new_workout_day_exercise = db.query(WorkoutDayExerciseModel).filter(
                    WorkoutDayExerciseModel.id == exercise_configuration.workout_day_exercise_id
                ).first()
                
                if not new_workout_day_exercise:
                    return JSONResponse(
                        content={            
                            "message": "El nuevo ejercicio por día de la semana no fue encontrado",            
                            "data": None        
                            }, 
                            status_code=status.HTTP_404_NOT_FOUND
                        )
                
                new_training_plan = db.query(TrainingPlanModel).filter(
                    TrainingPlanModel.id == new_workout_day_exercise.training_plan_id
                ).first()
                
                if not new_training_plan:
                    return JSONResponse(
                        content={            
                            "message": "El plan de entrenamiento del nuevo ejercicio no fue encontrado",            
                            "data": None        
                            }, 
                            status_code=status.HTTP_404_NOT_FOUND
                        )
                
                if new_training_plan.user_email != current_user and role_user != 4:
                    return JSONResponse(
                        content={            
                            "message": "No tienes permiso para asignar esta configuración a un ejercicio que no es tuyo",            
                            "data": None        
                            }, 
                            status_code=status.HTTP_403_FORBIDDEN
                        )
                
            # Actualizar la configuración
            try:
                element = ExerciseConfigurationRepository(db).update_exercise_configuration(id, exercise_configuration)  
                return JSONResponse(
                    content={        
                        "message": "The exercise configuration was successfully updated",        
                        "data": jsonable_encoder(element)    
                    }, 
                    status_code=status.HTTP_200_OK
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
            return JSONResponse(content={"message": "User is inactive"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Insufficient privileges"}, status_code=status.HTTP_403_FORBIDDEN)