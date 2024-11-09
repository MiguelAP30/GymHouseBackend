from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.repositories.exercise import ExerciseRepository
from src.schemas.exercise import Exercise
from src.models.exercise import Exercise as ExerciseModel
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

exercise_router = APIRouter(tags=['Ejercicios'])

#CRUD exercise

@exercise_router.get('/',response_model=List[Exercise],description="Devuelve todos los ejercicios")
def get_exercises(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[Exercise]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3:
            if status_user:
                result = ExerciseRepository(db).get_all_excercises()
                return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@exercise_router.get('/{id}',response_model=Exercise,description="Devuelve la información de un solo ejercicio")
def get_excercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> Exercise:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3:
            if status_user:
                element=  ExerciseRepository(db).get_excercise_by_id(id)
                if not element:        
                    return JSONResponse(
                        content={            
                            "message": "The requested exercise was not found",            
                            "data": None        
                            }, 
                        status_code=status.HTTP_404_NOT_FOUND
                        )    
                return JSONResponse(
                    content=jsonable_encoder(element),                        
                    status_code=status.HTTP_200_OK
                    )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@exercise_router.post('/',response_model=dict,description="Crear un nuevo ejercicio")
def create_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], exercise: Exercise = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3:
            if status_user:
                new_excercise = ExerciseRepository(db).create_new_excercise(exercise)
                return JSONResponse(
                    content={        
                    "message": "The exercise was successfully created",        
                    "data": jsonable_encoder(new_excercise)    
                    }, 
                    status_code=status.HTTP_201_CREATED
                )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@exercise_router.delete('/{id}',response_model=dict,description="Remover un ejercicio específico")
def remove_excercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3:
            if status_user:
                element = ExerciseRepository(db).delete_excercise(id)
                if not element:        
                    return JSONResponse(
                        content={            
                            "message": "The requested exercise was not found",            
                            "data": None        
                            }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
                return JSONResponse(
                    content={        
                    "message": "The exercise was successfully removed",        
                    "data": jsonable_encoder(element)    
                    }, 
                    status_code=status.HTTP_200_OK
                )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@exercise_router.put('/{id}',response_model=Exercise,description="Actualizar un ejercicio específico")
def update_excercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), exercise: Exercise = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3:
            if status_user:
                element = ExerciseRepository(db).update_excercise(id, exercise)
                if not element:        
                    return JSONResponse(
                        content={            
                            "message": "The requested exercise was not found",            
                            "data": None        
                            }, 
                        status_code=status.HTTP_404_NOT_FOUND
                    )
                return JSONResponse(
                    content={        
                    "message": "The exercise was successfully updated",        
                    "data": jsonable_encoder(element)    
                    }, 
                    status_code=status.HTTP_200_OK
                )
            else:
                return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
