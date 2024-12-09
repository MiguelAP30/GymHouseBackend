from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.comment import Comment
from src.repositories.comment import CommentRepository
from src.models.comment import Comment as comments

comment_router = APIRouter(tags=['Comentarios'])

#CRUD comment

@comment_router.post('',response_model=Comment,description="Crea un nuevo comentario")
def create_comment(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], comment: Comment = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_comment = CommentRepository(db).create_new_comment(comment)
            return JSONResponse(
                content={        
                "message": "The comment was successfully created",        
                "data": jsonable_encoder(new_comment)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    
@comment_router.delete('/{id}',response_model=dict,description="Elimina un comentario específico")
def remove_comment(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = CommentRepository(db).delete_comment(id)
            return JSONResponse(content={"message": "The comment was successfully deleted", "data": result}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    
@comment_router.put('/{id}',response_model=Comment,description="Actualiza un comentario específico")
def update_comment(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), comment: Comment = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = CommentRepository(db).update_comment(id, comment)
            return JSONResponse(content={"message": "The comment was successfully updated", "data": result}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    
@comment_router.get('/{id}',response_model=Comment,description="Devuelve un comentario específico")
def get_comment_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = CommentRepository(db).get_comment_by_id(id)
            return JSONResponse(content={"message": "The comment was successfully found", "data": result}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    
@comment_router.get('/user/{id}',response_model=List[Comment],description="Devuelve todos los comentarios de un usuario")
def get_comment_by_user(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = CommentRepository(db).get_comment_by_user(id)
            return JSONResponse(content={"message": "The comment was successfully found", "data": result}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    
@comment_router.get('/training_plan/{id}',response_model=List[Comment],description="Devuelve todos los comentarios de un plan de entrenamiento")
def get_comment_by_training_plan(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = CommentRepository(db).get_comment_by_training_plan(id)
            return JSONResponse(content={"message": "The comment was successfully found", "data": result}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
