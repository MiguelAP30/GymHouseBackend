from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.training_plan import TrainingPlan
from src.models.training_plan import TrainingPlan as training_plans
from src.repositories.training_plan import TrainingPlanRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

training_plan_router = APIRouter(tags=['Planes de entrenamiento'])

#CRUD training_plan

@training_plan_router.get('',response_model=List[TrainingPlan],description="Retorna todos los planes de entrenamiento")
def get_training_plans(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[TrainingPlan]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        result = TrainingPlanRepository(db).get_all_training_plans()
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@training_plan_router.get('', response_model=List[TrainingPlan], description="Retorna todos los planes de entrenamiento de los usuarios con rol de administrador")
def get_training_plans_by_role_admin(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> List[TrainingPlan]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        result = TrainingPlanRepository(db).get_all_training_plans_by_role_admin()
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@training_plan_router.get('', response_model=List[TrainingPlan], description="Retorna todos los planes de entrenamiento de los usuarios con rol de administrador")
def get_training_plans_by_role_gym(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> List[TrainingPlan]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        result = TrainingPlanRepository(db).get_all_training_plans_by_role_gym()
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@training_plan_router.get('', response_model=List[TrainingPlan], description="Retorna todos los planes de entrenamiento de los usuarios con rol de administrador")
def get_training_plans_by_role_premium(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> List[TrainingPlan]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        result = TrainingPlanRepository(db).get_all_training_plans_by_role_premium()
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@training_plan_router.get('', response_model=List[TrainingPlan], description="Retorna todos los planes de entrenamiento creados por el usuario autenticado")
def get_my_training_plans(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> List[TrainingPlan]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        current_user_email = payload.get("sub")
        result = TrainingPlanRepository(db).get_all_my_training_plans(current_user_email)
        return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@training_plan_router.get('/{id}',response_model=TrainingPlan,description="Retorna un solo plan de entrenamiento")
def get_training_plan_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> TrainingPlan:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        current_user = payload.get("sub")
        element=  TrainingPlanRepository(db).get_training_plan_by_id(id, current_user)
        if not element:        
            return JSONResponse(
                content={            
                    "message": "The requested training plan was not found",            
                    "data": None        
                    }, 
                status_code=status.HTTP_404_NOT_FOUND
                )    
        return JSONResponse(
            content=jsonable_encoder(element),                        
            status_code=status.HTTP_200_OK
            )

@training_plan_router.post('',response_model=dict,description="Crea un nuevo plan de entrenamiento")
##Debe recibir el ID de ejercicio por día de la semana y de tag de plan de entrenamiento en el JSON que viene con el Frontend
def create_training_plan(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], training_plan: TrainingPlan = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user  = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        training_plan.user_email = payload.get("sub")
        new_training_plan = TrainingPlanRepository(db).create_new_training_plan(training_plan)
        return JSONResponse(
            content={        
            "message": "The training plan was successfully created",        
            "data": jsonable_encoder(new_training_plan)    
            }, 
            status_code=status.HTTP_201_CREATED
        )

@training_plan_router.delete('/{id}', response_model=dict, description="Elimina un plan de entrenamiento específico")
def remove_training_plan(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        current_user = payload.get("sub")
        element = TrainingPlanRepository(db).get_training_plan_by_id(id, current_user)
        if not element:
            return JSONResponse(content={"message": "The requested training plan was not found", "data": None}, status_code=status.HTTP_404_NOT_FOUND)
        if element.user_email != current_user:
            return JSONResponse(content={"message": "You do not have the necessary permissions to delete this training plan", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        TrainingPlanRepository(db).delete_training_plan(id, current_user)
        return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)

@training_plan_router.put('/{id}', response_model=dict, description="Actualiza un plan de entrenamiento específico")
def update_training_plan(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1), training_plan: TrainingPlan = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user == False:
            return JSONResponse(content={"message": "Your account is disabled", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        current_user = payload.get("sub")
        element = TrainingPlanRepository(db).get_training_plan_by_id(id, current_user)
        if not element:
            return JSONResponse(content={"message": "The requested training plan was not found", "data": None}, status_code=status.HTTP_404_NOT_FOUND)
        if element.user_email != current_user:
            return JSONResponse(content={"message": "You do not have the necessary permissions to update this training plan", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        updated_element = TrainingPlanRepository(db).update_training_plan(id, training_plan, current_user)
        return JSONResponse(content=jsonable_encoder(updated_element), status_code=status.HTTP_200_OK)