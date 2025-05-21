from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.profile import Profile, ProfileUpdate
from src.repositories.profile import ProfileRepository
from src.models.profile import Profile as profiles

profile_router = APIRouter(tags=['Perfil'])

#CRUD profile

@profile_router.get('',response_model=List[Profile],description="Devuelve todos los perfiles")
def get_profile(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[Profile]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 1:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = ProfileRepository(db).get_all_profile()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@profile_router.post('',response_model=Profile,description="Crea un nuevo perfil")
def create_profile(profile: Profile, credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> Profile:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        user_email = payload.get("sub")
        if role_current_user < 1:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            profile.user_email = user_email
            result = ProfileRepository(db).create_new_profile(profile)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@profile_router.delete('/{id}',description="Elimina un perfil específico")
def delete_profile(id: int, credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> dict:
    db= SessionLocal()
    try:
        payload = auth_handler.decode_token(credentials.credentials)
        if payload:
            role_current_user = payload.get("user.role")
            user_status = payload.get("user.status")
            if role_current_user < 1:
                return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
            if user_status:
                result = ProfileRepository(db).delete_profile(id)
                if result:
                    return JSONResponse(
                        content={"message": "Perfil eliminado exitosamente", "data": jsonable_encoder(result)},
                        status_code=status.HTTP_200_OK
                    )
                return JSONResponse(
                    content={"message": "Perfil no encontrado"},
                    status_code=status.HTTP_404_NOT_FOUND
                )
            return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return JSONResponse(
            content={"message": "Error al eliminar el perfil", "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        db.close()

@profile_router.put('/{id}',response_model=Profile,description="Actualiza un perfil específico")
def update_profile(id: int, profile: ProfileUpdate, credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> Profile:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 1:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = ProfileRepository(db).update_profile(id,profile)
            if result:
                return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
            return JSONResponse(content={"message": "Perfil no encontrado"}, status_code=status.HTTP_404_NOT_FOUND)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@profile_router.get('/{email}',response_model=Profile,description="Devuelve un perfil específico")
def get_profile_by_email(email: str, credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> Profile:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 1:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = ProfileRepository(db).get_profile_by_email(email)
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@profile_router.get('/id/{id}', response_model=Profile, description="Obtiene un perfil específico por su ID")
def get_profile_by_id(id: int, credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> Profile:
    db = SessionLocal()
    try:
        payload = auth_handler.decode_token(credentials.credentials)
        if payload:
            role_current_user = payload.get("user.role")
            user_status = payload.get("user.status")
            if role_current_user < 1:
                return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
            if user_status:
                result = ProfileRepository(db).get_profile_by_id(id)
                if result:
                    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
                return JSONResponse(
                    content={"message": "Perfil no encontrado"},
                    status_code=status.HTTP_404_NOT_FOUND
                )
            return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return JSONResponse(
            content={"message": "Error al obtener el perfil", "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        db.close()
