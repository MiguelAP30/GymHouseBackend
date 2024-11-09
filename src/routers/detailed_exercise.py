from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.detailed_exercise import DetailedExercise
from src.repositories.detailed_exercise import DetailedExerciseRepository
from src.models.detailed_exercise import DetailedExercise as detailed_exercises



detailed_exercise_router = APIRouter(tags=['Ejercicios detallados'])

#CRUD detailed_exercise

@detailed_exercise_router.get('/',response_model=List[DetailedExercise],description="Devuelve todos los ejercicios detallados")
def get_detailed_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[DetailedExercise]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            current_user = payload.get("sub")
            result = DetailedExerciseRepository(db).get_all_detailed_exercise(current_user)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@detailed_exercise_router.post('/',response_model=DetailedExercise,description="Crea un nuevo ejercicio detallado")
def create_detailed_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], detailed_exercise: DetailedExercise = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_detailed_exercise = DetailedExerciseRepository(db).create_new_detailed_exercise(detailed_exercise)
            return JSONResponse(
                content={        
                "message": "The detailed exercise was successfully created",        
                "data": jsonable_encoder(new_detailed_exercise)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@detailed_exercise_router.delete('/{id}',response_model=dict,description="Elimina un ejercicio detallado específico")
def remove_detailed_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            current_user = payload.get("sub")
            DetailedExerciseRepository(db).delete_detailed_exercise(id, current_user)
            return JSONResponse(
                content={        
                "message": "The detailed exercise was successfully deleted",        
                "data": None    
                }, 
                status_code=status.HTTP_200_OK
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@detailed_exercise_router.get('/{id}',response_model=DetailedExercise,description="Devuelve un ejercicio detallado específico")
def get_detailed_exercise_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            current_user = payload.get("sub")
            element=  DetailedExerciseRepository(db).get_detailed_exercise_by_id(id, current_user)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested detailed exercise was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content=jsonable_encoder(element),                        
                status_code=status.HTTP_200_OK
                )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@detailed_exercise_router.put('/{id}',response_model=DetailedExercise,description="Actualiza un ejercicio detallado específico")
def update_detailed_exercise(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), detailed_exercise: DetailedExercise = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            current_user = payload.get("sub")
            element = DetailedExerciseRepository(db).update_detailed_exercise(id, current_user, detailed_exercise)
            return JSONResponse(
                content={        
                "message": "The detailed exercise was successfully updated",        
                "data": jsonable_encoder(element)    
                }, 
                status_code=status.HTTP_200_OK
            )