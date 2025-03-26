from fastapi import APIRouter, Body, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Annotated, List
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

from src.schemas.specific_muscle import SpecificMuscle
from src.repositories.specific_muscle import SpecificMuscleRepository
from src.models.specific_muscle import SpecificMuscle as specific_muscle

specific_muscle_router = APIRouter(tags=['SpecificMuscle'])

#CRUD specific_muscle

@specific_muscle_router.get('',response_model=List[SpecificMuscle],description="Devuelve todos los músculos específicos")
def get_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[SpecificMuscle]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = SpecificMuscleRepository(db).get_all_specific_muscle()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.post('',response_model=SpecificMuscle,description="Crea un nuevo músculo específico")
def create_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], specific_muscle: SpecificMuscle = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            new_specific_muscle = SpecificMuscleRepository(db).create_new_specific_muscle(specific_muscle)
            return JSONResponse(
                content={        
                "message": "The specific_muscle was successfully created",        
                "data": jsonable_encoder(new_specific_muscle)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.delete('/{id}',response_model=dict,description="Elimina un músculo específico específico")
def remove_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            SpecificMuscleRepository(db).delete_specific_muscle(id)
            return JSONResponse(content={"message": "The specific_muscle was successfully deleted", "data": None}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.put('/{id}',response_model=SpecificMuscle,description="Actualiza un músculo específico específico")
def update_specific_muscle(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), specific_muscle: SpecificMuscle = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            updated_specific_muscle = SpecificMuscleRepository(db).update_specific_muscle(id, specific_muscle)
            return JSONResponse(
                content={        
                "message": "The specific_muscle was successfully updated",        
                "data": jsonable_encoder(updated_specific_muscle)    
                }, 
                status_code=status.HTTP_200_OK
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.get('/{id}',response_model=SpecificMuscle,description="Devuelve un músculo específico específico")
def get_specific_muscle_by_id(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            result = SpecificMuscleRepository(db).get_specific_muscle_by_id(id)
            return JSONResponse(content={"message": "The specific_muscle was successfully obtained", "data": jsonable_encoder(result)}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@specific_muscle_router.post('/init', response_model=dict, description="Inicializa músculos específicos en la base de datos")
def init_specific_muscles(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)]) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        status_user = payload.get("user.status")
        if role_current_user < 2:
            return JSONResponse(content={"message": "You do not have the necessary permissions", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if status_user:
            specific_muscles_data = [
                {"name": "Pectoral Mayor", "muscle_id": 1, "description": "Músculo principal del pecho, responsable de la aducción y rotación interna del brazo."},
                {"name": "Pectoral Menor", "muscle_id": 1, "description": "Músculo pequeño bajo el pectoral mayor, responsable de la estabilización de la escápula."},
                {"name": "Trapecio", "muscle_id": 2, "description": "Músculo grande en la parte superior de la espalda, encargado de los movimientos de la escápula."},
                {"name": "Dorsal Ancho", "muscle_id": 2, "description": "Músculo principal de la espalda, responsable de la extensión y aducción del brazo."},
                {"name": "Deltoides Anterior", "muscle_id": 3, "description": "Parte frontal del músculo del hombro, involucrado en la flexión del brazo."},
                {"name": "Bíceps", "muscle_id": 4, "description": "Músculo en la parte frontal del brazo, encargado de la flexión del codo y la supinación del antebrazo."},
                {"name": "Tríceps", "muscle_id": 4, "description": "Músculo en la parte posterior del brazo, encargado de la extensión del codo."},
                {"name": "Flexores del Antebrazo", "muscle_id": 5, "description": "Músculos encargados de la flexión de la muñeca y los dedos."},
                {"name": "Extensores del Antebrazo", "muscle_id": 5, "description": "Músculos encargados de la extensión de la muñeca y los dedos."},
                {"name": "Recto Abdominal", "muscle_id": 6, "description": "Músculo frontal del abdomen, responsable de la flexión del tronco."},
                {"name": "Oblicuos Externos", "muscle_id": 6, "description": "Músculos laterales del abdomen, responsables de la rotación y flexión lateral del tronco."},
                {"name": "Erector de la Columna", "muscle_id": 7, "description": "Músculos largos a lo largo de la columna vertebral, encargados de su extensión y estabilidad."},
                {"name": "Glúteo Mayor", "muscle_id": 8, "description": "Músculo más grande de los glúteos, encargado de la extensión de la cadera."},
                {"name": "Cuádriceps", "muscle_id": 9, "description": "Grupo muscular en la parte frontal del muslo, responsable de la extensión de la rodilla."},
                {"name": "Isquiotibiales", "muscle_id": 9, "description": "Grupo muscular en la parte posterior del muslo, encargado de la flexión de la rodilla y extensión de la cadera."},
                {"name": "Aductor Mayor", "muscle_id": 10, "description": "Músculo principal en la parte interna del muslo, responsable de la aducción de la pierna."},
                {"name": "Gastrocnemio", "muscle_id": 11, "description": "Músculo grande en la pantorrilla, responsable de la flexión plantar del pie."},
                {"name": "Sóleo", "muscle_id": 11, "description": "Músculo profundo en la pantorrilla, que también contribuye a la flexión plantar del pie."},
                {"name": "Supraespinoso", "muscle_id": 2, "description": "Músculo del manguito rotador responsable de la abducción del brazo."},
                {"name": "Romboides", "muscle_id": 2, "description": "Músculos entre la escápula y la columna vertebral, responsables de la retracción de la escápula."},
                {"name": "Erectores Espinales", "muscle_id": 2, "description": "Grupo de músculos largos a lo largo de la columna vertebral, encargados de su extensión y estabilización."},
                {"name": "Redondo Mayor", "muscle_id": 2, "description": "Músculo en la parte inferior del omóplato, responsable de la extensión y aducción del brazo."},
                {"name": "Redondo Menor", "muscle_id": 2, "description": "Músculo del manguito rotador, involucrado en la rotación externa del brazo."},
                {"name": "Infraespinoso", "muscle_id": 2, "description": "Músculo del manguito rotador que contribuye a la rotación externa del brazo."},
                {"name": "Deltoides Medio", "muscle_id": 3, "description": "Parte media del músculo del hombro, encargada de la abducción del brazo."},
                {"name": "Deltoides Posterior", "muscle_id": 3, "description": "Parte posterior del músculo del hombro, involucrada en la extensión y rotación externa del brazo."},
                {"name": "Oblicuos Internos", "muscle_id": 6, "description": "Músculos en los laterales del abdomen, responsables de la flexión lateral y rotación del tronco."},
                {"name": "Transverso Abdominal", "muscle_id": 6, "description": "Músculo profundo del abdomen, encargado de la compresión del abdomen y estabilidad del core."},
                {"name": "Cuadrado Lumbar", "muscle_id": 7, "description": "Músculo profundo en la parte baja de la espalda, responsable de la estabilización y flexión lateral del tronco."},
                {"name": "Glúteo Medio", "muscle_id": 8, "description": "Músculo en la parte lateral de la cadera, encargado de la abducción de la pierna y estabilización de la pelvis."},
                {"name": "Glúteo Menor", "muscle_id": 8, "description": "Músculo debajo del glúteo medio, involucrado en la abducción y rotación interna de la pierna."},
                {"name": "Aductor Largo", "muscle_id": 10, "description": "Músculo en la parte interna del muslo, responsable de la aducción de la pierna."},
                {"name": "Aductor Corto", "muscle_id": 10, "description": "Músculo más profundo del aductor largo, encargado de la aducción y rotación externa de la pierna."},
                {"name": "Grácil", "muscle_id": 10, "description": "Músculo delgado en la parte interna del muslo, responsable de la aducción de la pierna y flexión de la rodilla."}
            ]
            
            created_specific_muscles = []
            for specific_muscle_data in specific_muscles_data:
                if not db.query(specific_muscle).filter_by(name=specific_muscle_data["name"]).first():
                    new_specific_muscle = specific_muscle(**specific_muscle_data)
                    db.add(new_specific_muscle)
                    created_specific_muscles.append(new_specific_muscle)
            
            db.commit()
            return JSONResponse(
                content={
                    "message": "Los músculos específicos se han inicializado correctamente",
                    "data": jsonable_encoder(created_specific_muscles)
                },
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Your account is inactive", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

