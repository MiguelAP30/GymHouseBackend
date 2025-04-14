from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.repositories.exercise_muscle import ExerciseMuscleRepository
from src.schemas.exercise_muscle import ExerciseMuscle, ExerciseMuscleAssignment
from src.models.exercise_muscle import ExerciseMuscle as ExcersiceMuscleModel
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

exercise_muscle_router = APIRouter(tags=['Máquina para hacer ejercicio por músculo'])

#CRUD exercise_muscle_router

@exercise_muscle_router.get('', response_model=List[ExerciseMuscle], description="Obtiene todos los ejercicios-músculos ordenados por calificación")
def get_all_excercise_muscle_by_rate(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> List[ExerciseMuscle]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExerciseMuscleRepository(db).get_all_excercise_muscle_by_rate()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.get('/machine/{machine_id}', response_model=List[ExerciseMuscle], description="Obtiene todos los ejercicios-músculos de una máquina específica ordenados por calificación")
def get_all_excercise_muscle_machine_by_rate(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], machine_id: int = Path(ge=1)) -> List[ExerciseMuscle]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExerciseMuscleRepository(db).get_excercise_muscle_machine_by_rate(machine_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.get('/specific-muscle/{specific_muscle_id}', response_model=List[ExerciseMuscle], description="Obtiene todos los ejercicios-músculos de un músculo específico ordenados por calificación")
def get_all_excercise_muscle_specific_muscle_by_rate(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], specific_muscle_id: int = Path(ge=1)) -> List[ExerciseMuscle]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExerciseMuscleRepository(db).get_excercise_muscle_specific_muscle_by_rate(specific_muscle_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.get('/muscle/{muscle_id}', response_model=List[ExerciseMuscle], description="Obtiene todos los ejercicios-músculos de un músculo general ordenados por calificación")
def get_all_excercise_muscle_by_muscle_by_rate(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], muscle_id: int = Path(ge=1)) -> List[ExerciseMuscle]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExerciseMuscleRepository(db).get_excercise_muscle_by_muscle_by_rate(muscle_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.get('/{id}', response_model=ExerciseMuscle, description="Obtiene un ejercicio-músculo específico por su ID")
def get_excercise_muscle_machine(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> ExerciseMuscle:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            element = ExerciseMuscleRepository(db).get_excercise_muscle_by_id(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested exercise-muscle-machine was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content=jsonable_encoder(element),                        
                status_code=status.HTTP_200_OK
                )
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.post('', response_model=dict, description="Crea un nuevo ejercicio-musculo-maquina")
def create_excercise_muscle_machine(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], exercise: ExerciseMuscle = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            new_excercise = ExerciseMuscleRepository(db).create_new_excercise_muscle(exercise)
            return JSONResponse(
                content={        
                "message": "The exercise-muscle-machine was successfully created",        
                "data": jsonable_encoder(new_excercise)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.delete('/{id}', response_model=dict, description="Elimina un ejercicio-musculo-maquina por id")
def remove_excercise_muscle_machine(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            element = ExerciseMuscleRepository(db).delete_excercise_muscle(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested exercise-muscle-machine was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content={        
                "message": "The exercise-muscle-machine was successfully removed",        
                "data": jsonable_encoder(element)    
                }, 
                status_code=status.HTTP_200_OK
            )
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.put('/{id}', response_model=dict, description="Actualiza un ejercicio-musculo-maquina por id")
def update_excercise_muscle_machine(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1), exercise: ExerciseMuscle = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            try:
                element = ExerciseMuscleRepository(db).update_exercise_muscle(id, exercise)
                if not element:        
                    return JSONResponse(
                        content={            
                            "message": "The requested exercise-muscle-machine was not found",            
                            "data": None        
                            }, 
                        status_code=status.HTTP_404_NOT_FOUND
                        )    
                return JSONResponse(
                    content={        
                    "message": "The exercise-muscle-machine was successfully updated",        
                    "data": jsonable_encoder(element)    
                    }, 
                    status_code=status.HTTP_200_OK
                )
            except Exception as e:
                return JSONResponse(
                    content={            
                        "message": f"Error al actualizar el ejercicio-músculo: {str(e)}",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_400_BAD_REQUEST
                    )
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.post('/assign-muscles', response_model=dict, description="Asigna múltiples músculos a un ejercicio con sus respectivas tasas de intensidad")
def assign_muscles_to_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], assignment: ExerciseMuscleAssignment = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            try:
                result = ExerciseMuscleRepository(db).assign_muscles_to_exercise(assignment)
                return JSONResponse(
                    content={        
                    "message": "Los músculos fueron asignados correctamente al ejercicio",        
                    "data": jsonable_encoder(result)    
                    }, 
                    status_code=status.HTTP_201_CREATED
                )
            except Exception as e:
                return JSONResponse(
                    content={            
                        "message": f"Error al asignar músculos al ejercicio: {str(e)}",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_400_BAD_REQUEST
                    )
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.get('/exercise/{exercise_id}/muscles', response_model=List[ExerciseMuscle], description="Obtiene todos los músculos asignados a un ejercicio específico")
def get_muscles_by_exercise(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], exercise_id: int = Path(ge=1)) -> List[ExerciseMuscle]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = ExerciseMuscleRepository(db).get_muscles_by_exercise(exercise_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )

@exercise_muscle_router.patch('/{id}/rate', response_model=dict, description="Actualiza solo la tasa de un ejercicio-músculo")
def update_exercise_muscle_rate(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1), rate: int = Body(..., ge=0, le=10)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            try:
                element = ExerciseMuscleRepository(db).update_exercise_muscle(id, rate)
                if not element:        
                    return JSONResponse(
                        content={            
                            "message": "The requested exercise-muscle was not found",            
                            "data": None        
                            }, 
                        status_code=status.HTTP_404_NOT_FOUND
                        )    
                return JSONResponse(
                    content={        
                    "message": "The exercise-muscle rate was successfully updated",        
                    "data": jsonable_encoder(element)    
                    }, 
                    status_code=status.HTTP_200_OK
                )
            except Exception as e:
                return JSONResponse(
                    content={            
                        "message": f"Error al actualizar la tasa del ejercicio-músculo: {str(e)}",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_400_BAD_REQUEST
                    )
        elif not status_user:
            return JSONResponse(
                content={            
                    "message": "Your account is inactive",            
                    "data": None        
                    }, 
                status_code=status.HTTP_403_FORBIDDEN
                )
        else:
            return JSONResponse(
                content={            
                    "message": "You do not have the necessary permissions",            
                    "data": None        
                    }, 
                status_code=status.HTTP_401_UNAUTHORIZED
                )
