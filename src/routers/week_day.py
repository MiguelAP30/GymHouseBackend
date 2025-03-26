from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi import APIRouter
from src.config.database import SessionLocal 
from fastapi.encoders import jsonable_encoder
from src.schemas.week_day import WeekDay
from src.models.week_day import WeekDay as WeekDayModel
from src.repositories.week_day import WeekDayRepository
from src.auth.has_access import security
from src.auth import auth_handler
from fastapi.security import HTTPAuthorizationCredentials

week_day_router = APIRouter(tags=['Días de la semana'])

#CRUD week_day

@week_day_router.get('',response_model=List[WeekDay],description="Devuelve todos los días de la semana")
def get_week_days(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)])-> List[WeekDay]:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 1:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            result = WeekDayRepository(db).get_all_week_days()
            return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@week_day_router.get('/{id}',response_model=WeekDay,description="Devuelve la información de un solo día de la semana")
def get_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> WeekDay:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 1:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            element = WeekDayRepository(db).get_week_day_by_id(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "El día de la semana solicitado no fue encontrado",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )    
            return JSONResponse(
                content=jsonable_encoder(element),                        
                status_code=status.HTTP_200_OK
                )
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@week_day_router.post('',response_model=dict,description="Crea un nuevo día de la semana")
def create_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], week_day: WeekDay = Body()) -> dict:
    db= SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 3:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            new_week_day = WeekDayRepository(db).create_new_week_day(week_day)
            return JSONResponse(
                content={        
                "message": "El día de la semana fue creado exitosamente",        
                "data": jsonable_encoder(new_week_day)    
                }, 
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@week_day_router.delete('/{id}',response_model=dict,description="Elimina un día de la semana específico")
def remove_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 4:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            element = WeekDayRepository(db).delete_week_day(id)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "El día de la semana solicitado no fue encontrado",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@week_day_router.put('/{id}',response_model=dict,description="Actualiza un día de la semana específico")
def update_week_day(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)], id: int = Path(ge=1), week_day: WeekDay = Body()) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 4:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            element = WeekDayRepository(db).update_week_day(id, week_day)
            if not element:        
                return JSONResponse(
                    content={            
                        "message": "El día de la semana solicitado no fue encontrado",            
                        "data": None        
                        }, 
                    status_code=status.HTTP_404_NOT_FOUND
                    )
            return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)

@week_day_router.post('/init', response_model=dict, description="Inicializa los 7 días de la semana en la base de datos")
def init_week_days(credentials: Annotated[HTTPAuthorizationCredentials,Depends(security)]) -> dict:
    db = SessionLocal()
    payload = auth_handler.decode_token(credentials.credentials)
    if payload:
        role_current_user = payload.get("user.role")
        user_status = payload.get("user.status")
        if role_current_user < 4:
            return JSONResponse(content={"message": "No tienes los permisos necesarios", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)
        if user_status:
            days = [
                {"name": "Lunes"},
                {"name": "Martes"},
                {"name": "Miércoles"},
                {"name": "Jueves"},
                {"name": "Viernes"},
                {"name": "Sábado"},
                {"name": "Domingo"}
            ]
            
            created_days = []
            for day in days:
                if not db.query(WeekDayModel).filter_by(name=day["name"]).first():
                    new_day = WeekDayModel(**day)
                    db.add(new_day)
                    created_days.append(new_day)
            
            db.commit()
            return JSONResponse(
                content={
                    "message": "Los días de la semana se han inicializado correctamente",
                    "data": jsonable_encoder(created_days)
                },
                status_code=status.HTTP_201_CREATED
            )
        return JSONResponse(content={"message": "Tu cuenta está inactiva", "data": None}, status_code=status.HTTP_401_UNAUTHORIZED)