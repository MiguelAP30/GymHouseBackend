from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.like import Like, LikeResponse
from src.models.like import Like as LikeModel
from src.models.training_plan import TrainingPlan as TrainingPlanModel
from src.models.user import User as UserModel
from src.repositories.like import LikeRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler

like_router = APIRouter(tags=['Likes'])

@like_router.post('', response_model=dict, description="Crea un nuevo like/dislike")
def create_like(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], like: Like = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            like.user_email = current_user
            new_like = LikeRepository(db).create_like(like)
            return JSONResponse(
                content={        
                "message": "El like/dislike fue creado exitosamente",        
                "data": jsonable_encoder(new_like)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@like_router.get('/training-plan/{training_plan_id}', response_model=List[LikeResponse], description="Obtiene todos los likes/dislikes de un plan de entrenamiento")
def get_likes_by_training_plan(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], training_plan_id: int = Path(ge=1)) -> List[LikeResponse]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = LikeRepository(db).get_likes_by_training_plan(training_plan_id)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@like_router.get('/user/{user_email}', response_model=List[LikeResponse], description="Obtiene todos los likes/dislikes de un usuario")
def get_likes_by_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], user_email: str = Path(min_length=5)) -> List[LikeResponse]:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            result = LikeRepository(db).get_likes_by_user(user_email)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@like_router.delete('/{id}', response_model=dict, description="Elimina un like/dislike específico")
def remove_like(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            current_user = payload.get("sub")
            element = LikeRepository(db).get_like_by_id(id)
            if not element:
                return JSONResponse(
                    content={            
                        "message": "El like/dislike solicitado no fue encontrado",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )
            if element.user_email != current_user:
                return JSONResponse(
                    content={            
                        "message": "No tienes permiso para eliminar este like/dislike",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_403_FORBIDDEN
                    )
            LikeRepository(db).remove_like(id)
            return JSONResponse(
                content={        
                "message": "El like/dislike fue eliminado exitosamente",        
                "data": None    
                }, 
                status_code=status.HTTP_200_OK
            )
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@like_router.get('/training-plan/{training_plan_id}/count', response_model=dict, description="Obtiene el conteo de likes/dislikes de un plan de entrenamiento")
def get_training_plan_likes_count(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], training_plan_id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            likes = LikeRepository(db).get_training_plan_likes_count(training_plan_id)
            dislikes = LikeRepository(db).get_training_plan_dislikes_count(training_plan_id)
            return JSONResponse(
                content={
                    "likes": likes,
                    "dislikes": dislikes,
                    "total": likes + dislikes
                },
                status_code=status.HTTP_200_OK
            )
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)

@like_router.get('/user/{user_email}/training-plan/{training_plan_id}/status', response_model=dict, description="Obtiene el estado del like/dislike de un usuario para un plan de entrenamiento")
def get_user_like_status(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], user_email: str = Path(min_length=5), training_plan_id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 2 and status_user:
            like_status = LikeRepository(db).get_user_like_status(user_email, training_plan_id)
            if like_status is None:
                return JSONResponse(
                    content={"status": "none"},
                    status_code=status.HTTP_200_OK
                )
            return JSONResponse(
                content={"status": "like" if like_status else "dislike"},
                status_code=status.HTTP_200_OK
            )
        elif not status_user:
            return JSONResponse(content={"message": "Usuario inactivo"}, status_code=status.HTTP_403_FORBIDDEN)
        else:
            return JSONResponse(content={"message": "Privilegios insuficientes"}, status_code=status.HTTP_403_FORBIDDEN)