from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.muscle import Muscle
from src.models.muscle import Muscle as muscles
from src.repositories.muscle import MuscleRepository
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler


muscle_router = APIRouter(tags=['Músculos'])

#CRUD muscle

@muscle_router.get('',response_model=List[Muscle],description="Devuelve todos los músculos")
def get_muscles(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[Muscle]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            result = MuscleRepository(db).get_all_muscles()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
    
@muscle_router.get('/{id}',response_model=Muscle,description="Devuelve la información de un solo músculo")
def get_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> Muscle:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            element=  MuscleRepository(db).get_muscle_by_id(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested muscle was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content=jsonable_encoder(element),                        
                status_code=status.HTTP_200_OK
                )
        return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@muscle_router.post('',response_model=dict,description="Crea un nuevo músculo")
def create_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], muscle: Muscle = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            new_muscle = MuscleRepository(db).create_new_muscle(muscle)
            return JSONResponse(
                content={        
                "message": "The muscle was successfully created",        
                "data": jsonable_encoder(new_muscle)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@muscle_router.delete('/{id}',response_model=dict,description="Elimina un músculo específico")
def remove_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            element = MuscleRepository(db).delete_muscle(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested muscle was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@muscle_router.put('/{id}',response_model=dict,description="Actualiza un músculo específico")
def update_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), muscle: Muscle = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            element = MuscleRepository(db).update_muscle(id, muscle)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "The requested muscle was not found",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@muscle_router.post('/init', response_model=dict, description="Inicializa músculos específicos en la base de datos")
def init_muscles(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)]) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_user >= 3 and status_user:
            muscles_data = [
                {"name": "Pecho", "description": "Grupo muscular en la parte delantera del torso, responsable de movimientos de empuje."},
                {"name": "Espalda", "description": "Grupo muscular en la parte posterior del torso, involucrado en movimientos de tracción y estabilización."},
                {"name": "Hombros", "description": "Grupo muscular ubicado en la parte superior del brazo, clave en movimientos de empuje y elevación."},
                {"name": "Brazos", "description": "Grupo muscular que incluye los músculos en la parte superior del brazo, responsable de flexión y extensión del codo."},
                {"name": "Antebrazos", "description": "Músculos responsables de la flexión y extensión de la muñeca y los dedos."},
                {"name": "Abdomen", "description": "Grupo muscular en la parte frontal del torso, fundamental para la estabilidad del core y movimientos de flexión del tronco."},
                {"name": "Zona Lumbar", "description": "Músculos en la parte baja de la espalda, esenciales para la estabilidad y extensión de la columna."},
                {"name": "Glúteos", "description": "Grupo muscular en la parte posterior de la cadera, involucrado en la extensión de la cadera y estabilización."},
                {"name": "Muslos", "description": "Grupo muscular en la parte frontal y posterior del muslo, responsable de la extensión y flexión de la rodilla."},
                {"name": "Aductores", "description": "Grupo muscular en la parte interna del muslo, encargado de la aducción de la pierna."},
                {"name": "Pantorrillas", "description": "Músculos en la parte inferior de la pierna, responsables de la flexión plantar del pie."},
                {"name": "Serrato Anterior", "description": "Músculo en la parte lateral del torso, involucrado en la estabilización de la escápula."}
            ]
            
            created_muscles = []
            for muscle_data in muscles_data:
                if not db.query(muscles).filter_by(name=muscle_data["name"]).first():
                    new_muscle = muscles(**muscle_data)
                    db.add(new_muscle)
                    created_muscles.append(new_muscle)
            
            db.commit()
            return JSONResponse(
                content={
                    "message": "Los músculos se han inicializado correctamente",
                    "data": jsonable_encoder(created_muscles)
                },
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "You do not have the necessary permissions or your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
