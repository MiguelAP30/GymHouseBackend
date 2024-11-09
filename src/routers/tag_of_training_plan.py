from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.tag_of_training_plan import TagOfTrainingPlan
from src.models.tag_of_training_plan import TagOfTrainingPlan as tag_of_training_plans
from src.repositories.tag_of_training_plan import TagOfTrainingPlanRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

tag_of_training_plan_router = APIRouter(tags=['Etiquetas para planes de entrenamiento'])

#CRUD tag_of_training_plan

@tag_of_training_plan_router.get('/',response_model=List[TagOfTrainingPlan],description="Devuelve todas las etiquetas de planes de entrenamiento")
def get_tag(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[TagOfTrainingPlan]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_user >= 2 and user_status == True:
            result = TagOfTrainingPlanRepository(db).get_all_tag_of_training_plans()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@tag_of_training_plan_router.get('/{id}',response_model=TagOfTrainingPlan,description="Devuelve la información de una sola etiqueta de plan de entrenamiento")
def get_tag_of_training_plan(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> TagOfTrainingPlan:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user == True:
            element=  TagOfTrainingPlanRepository(db).get_tag_of_training_plan_by_id(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested tag of training plan was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content=jsonable_encoder(element),                        
                status_code=status.HTTP_200_OK
                )
        return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@tag_of_training_plan_router.post('/',response_model=dict,description="Crea una nueva etiqueta de plan de entrenamiento")
def create_tag(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], tag_of_training_plan: TagOfTrainingPlan = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_user >= 2 and user_status == True:
            new_tag_of_training_plan = TagOfTrainingPlanRepository(db).create_new_tag_of_training_plan(tag_of_training_plan)
            return JSONResponse(
                content={        
                "message": "The tag of training plan was successfully created",        
                "data": jsonable_encoder(new_tag_of_training_plan)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@tag_of_training_plan_router.delete('/{id}',response_model=dict,description="Elimina una etiqueta de plan de entrenamiento específica")
def remove_tag_of_training_plan(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_user >= 2 and user_status == True:
            element = TagOfTrainingPlanRepository(db).delete_tag_of_training_plan(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested tag of training plan was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@tag_of_training_plan_router.put('/{id}',response_model=TagOfTrainingPlan,description="Actualiza una etiqueta de plan de entrenamiento específica")
def update_tag_of_training_plan(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), tag_of_training_plan: TagOfTrainingPlan = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_user >= 2 and user_status == True:
            element = TagOfTrainingPlanRepository(db).update_tag_of_training_plan(id, tag_of_training_plan)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested tag of training plan was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)